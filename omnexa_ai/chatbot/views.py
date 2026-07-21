"""
Views for chatbot widget backend.
Stores sessions and messages. Integrated with Groq AI (via direct HTTP) for smart responses.
"""

import os
import uuid
import json
import logging
import urllib.request
import urllib.error
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import ChatSession, ChatMessage, ChatbotKnowledgeBase
from .serializers import (
    ChatSessionSerializer, ChatMessageSerializer,
    ChatbotKnowledgeBaseSerializer, ChatbotResponseSerializer
)
from omnexa_ai.core.utils import get_client_ip

logger = logging.getLogger(__name__)

# ── AI Setup (NVIDIA NIM - Kimi K2.6) ───────────────────────────────────────
NVIDIA_API_URL  = "https://integrate.api.nvidia.com/v1/chat/completions"
PRIMARY_MODEL   = "meta/llama-3.1-8b-instruct"    # fast & confirmed working

SYSTEM_PROMPT = (
    "You are the OMNEXA AI Assistant — a helpful, friendly, and professional AI chatbot "
    "for OMNEXA AI, a company that specializes in AI-powered business solutions. "
    "Your role is to help visitors learn about OMNEXA AI's services, answer their questions, "
    "and guide them toward booking a free strategy consultation. "
    "\n\nIMPORTANT DEFINITIONS FOR OMNEXA AI CONTEXT:"
    "\n- AEO = Answer Engine Optimization (NOT 'Authorized Economic Operator'). "
    "AEO helps businesses appear in AI-powered search tools like ChatGPT, Perplexity, and Google AI Overviews. It is the next evolution of SEO."
    "\n\nOMNEXA AI services include:"
    "\n1. AEO (Answer Engine Optimization) - Get found in AI search tools"
    "\n2. AI Marketing - Intelligent, data-driven marketing campaigns"
    "\n3. AI Software Development - Custom AI-powered applications"
    "\n4. AI Chatbots - 24/7 lead capture and customer support bots"
    "\n5. Content Creation - AI-assisted blogs, copy, and scripts"
    "\n6. Image & Video Generation - AI-generated visual content"
    "\n7. Blog Writing - SEO-optimized, high-quality articles"
    "\n8. Lead Generation - AI-powered prospect acquisition systems"
    "\n9. Meta Ads - AI-optimized Facebook and Instagram advertising"
    "\n10. Landing Page Optimization - Conversion-focused page design"
    "\n11. Social Media Marketing - Automated social media growth"
    "\n\nAlways be concise, warm, and end responses with a helpful next step. "
    "If someone asks about pricing, suggest booking a free consultation at /contact/. "
    "Keep responses under 150 words unless the question needs a detailed answer. "
    "Respond in the same language the user is writing in. "
    "Never confuse OMNEXA AI's AEO (Answer Engine Optimization) with other meanings of AEO."
)


def _call_ai(api_url: str, model: str, api_key: str, user_message: str) -> str | None:
    """Generic OpenAI-compatible API caller (works for Groq & NVIDIA)."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }).encode("utf-8")

    req = urllib.request.Request(
        api_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"[AI] ❌ HTTP {e.code} from {api_url[:40]}: {body[:150]}")
        logger.error(f"AI HTTP error {e.code}: {body[:150]}")
        return None
    except Exception as e:
        print(f"[AI] ❌ Error: {e}")
        logger.error(f"AI API error: {e}")
        return None


def generate_bot_response(user_message: str) -> str:
    """
    NVIDIA NIM - meta/llama-3.1-8b-instruct (fast, free, confirmed working).
    """
    nvidia_key = os.environ.get('NVIDIA_API_KEY', '') or getattr(settings, 'NVIDIA_API_KEY', '')
    nvidia_key = nvidia_key.strip()

    if not nvidia_key or not nvidia_key.startswith('nvapi-'):
        print("[AI] ❌ No valid NVIDIA key found.")
        return (
            "I'm having a little trouble connecting right now. "
            "Please try again in a moment, or reach us at /contact/ — we'd love to help! 🙏"
        )

    reply = _call_ai(NVIDIA_API_URL, PRIMARY_MODEL, nvidia_key, user_message)
    if reply:
        print(f"[Llama-3.1-8B ✅] {reply[:60]}...")
        return reply

    return (
        "I'm having a little trouble connecting right now. "
        "Please try again in a moment, or reach us at /contact/ — we'd love to help! 🙏"
    )


def generate_bot_response(user_message: str) -> str:
    """
    Generate a bot response using NVIDIA NIM GLM-5.2 AI exclusively.
    No static or rule-based fallback — always AI-powered answers.
    """
    ai_reply = _nvidia_response(user_message)
    if ai_reply:
        return ai_reply

    # Only if AI is completely unreachable (network/key issue)
    return (
        "I'm having a little trouble connecting right now. "
        "Please try again in a moment, or reach us directly at /contact/ — "
        "we'd love to help! 🙏"
    )


@csrf_exempt
@require_POST
def chat_message(request):
    """
    POST /api/v1/chatbot/message/

    Body: { "session_key": "abc123", "message": "How can you help me?", "page_url": "..." }

    Logic:
      1. Get or create ChatSession using session_key
      2. Save user message
      3. Generate bot response (rule-based or AI-powered)
      4. Save bot response
      5. Return JSON with bot reply
    """
    try:
        data = json.loads(request.body)
        session_key = data.get('session_key') or str(uuid.uuid4())
        user_message = data.get('message', '').strip()
        page_url = data.get('page_url', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        # Get or create session
        session, created = ChatSession.objects.get_or_create(
            session_key=session_key,
            defaults={
                'page_url': page_url,
                'user_agent': user_agent,
                'ip_address': get_client_ip(request),
            }
        )

        # Save user message
        user_msg = ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_message
        )

        # Generate bot response
        bot_reply = generate_bot_response(user_message)

        # Save bot response
        bot_msg = ChatMessage.objects.create(
            session=session,
            role='bot',
            content=bot_reply
        )

        return JsonResponse({
            'success': True,
            'session_key': session_key,
            'reply': bot_reply,
            'message_id': bot_msg.id,
            'session_created': created,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def chat_history(request):
    """
    GET /api/v1/chatbot/history/?session_key=abc123

    Returns chat history for a given session.
    """
    session_key = request.GET.get('session_key')

    if not session_key:
        return JsonResponse({'error': 'session_key is required'}, status=400)

    try:
        session = ChatSession.objects.get(session_key=session_key)
        messages = session.messages.all().order_by('created_at')

        return JsonResponse({
            'success': True,
            'session_key': session_key,
            'messages': [
                {
                    'id': msg.id,
                    'role': msg.role,
                    'content': msg.content,
                    'created_at': msg.created_at.isoformat(),
                }
                for msg in messages
            ],
        })

    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def clear_chat(request):
    """
    DELETE /api/v1/chatbot/clear/?session_key=abc123

    Clears chat history for a given session.
    """
    session_key = request.GET.get('session_key')

    if not session_key:
        return JsonResponse({'error': 'session_key is required'}, status=400)

    try:
        session = ChatSession.objects.get(session_key=session_key)
        session.messages.all().delete()
        session.is_active = True
        session.save()

        return JsonResponse({
            'success': True,
            'message': 'Chat history cleared',
        })

    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# --- REST API Views ---
class ChatSessionListAPIView(APIView):
    """
    GET /api/v1/chatbot/sessions/
    List all chat sessions (admin use).
    """

    def get(self, request):
        sessions = ChatSession.objects.all().order_by('-created_at')
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class ChatSessionDetailAPIView(APIView):
    """
    GET /api/v1/chatbot/sessions/<session_key>/
    Get details of a specific chat session.
    """

    def get(self, request, session_key):
        try:
            session = ChatSession.objects.get(session_key=session_key)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ChatbotKnowledgeBaseListAPIView(APIView):
    """
    GET /api/v1/chatbot/knowledge/
    List all knowledge base entries.
    """

    def get(self, request):
        knowledge = ChatbotKnowledgeBase.objects.filter(is_active=True).order_by('-priority')
        serializer = ChatbotKnowledgeBaseSerializer(knowledge, many=True)
        return Response(serializer.data)


class ChatbotAnalyticsAPIView(APIView):
    """
    GET /api/v1/chatbot/analytics/
    Get chatbot analytics data.
    """

    def get(self, request):
        from .models import ChatbotAnalytics

        today = timezone.now().date()
        analytics, created = ChatbotAnalytics.objects.get_or_create(
            date=today,
            defaults={
                'total_sessions': 0,
                'total_messages': 0,
                'unique_users': 0,
                'avg_session_duration': 0,
                'successful_conversations': 0,
                'failed_conversations': 0,
            }
        )

        # Update analytics
        analytics.total_sessions = ChatSession.objects.filter(
            created_at__date=today
        ).count()

        analytics.total_messages = ChatMessage.objects.filter(
            created_at__date=today
        ).count()

        analytics.unique_users = ChatSession.objects.filter(
            created_at__date=today
        ).values('ip_address').distinct().count()

        analytics.save()

        return Response({
            'date': analytics.date.isoformat(),
            'total_sessions': analytics.total_sessions,
            'total_messages': analytics.total_messages,
            'unique_users': analytics.unique_users,
            'avg_session_duration': analytics.avg_session_duration,
            'successful_conversations': analytics.successful_conversations,
            'failed_conversations': analytics.failed_conversations,
        })
