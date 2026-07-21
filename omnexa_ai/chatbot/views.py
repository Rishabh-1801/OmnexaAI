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

# ── AI Setup (NVIDIA NIM - openai/gpt-oss-120b) ─────────────────────────────
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL          = "openai/gpt-oss-120b"   # sole model — no fallback

SYSTEM_PROMPT = (
    "You are OMNEXA AI Assistant — a highly capable, intelligent, helpful, and friendly AI chatbot "
    "powered by OMNEXA AI. "
    "You answer ANY user questions accurately, thoroughly, and professionally like ChatGPT and Claude — "
    "including programming/coding (Python, JavaScript, HTML, etc.), business advice, math, writing, technical Q&A, "
    "and general knowledge. "
    "Use standard Markdown formatting (bold text, bullet points, clean code blocks with language tags, tables when helpful) "
    "so your responses are formatted cleanly and easy to read. "
    "\n\nOMNEXA AI CONTEXT & SERVICES:"
    "\nOMNEXA AI specializes in AI-powered business solutions including:"
    "\n1. AEO (Answer Engine Optimization) - Helps businesses get found in AI search tools like ChatGPT, Perplexity, & Google AI Overviews."
    "\n2. AI Marketing, AI Software Development, AI Chatbots, Content & Blog Creation, Image/Video Generation, Lead Generation, Meta Ads, and Social Media Automation."
    "\n\nGUIDELINES:"
    "\n- Always respond in the SAME language or dialect the user is writing in (English, Gujarati, Gujarati in Roman/Gujlish, Hinglish, etc.)."
    "\n- Provide comprehensive, accurate, step-by-step answers for code/technical questions."
    "\n- When relevant or when asked about growth/services/pricing, naturally offer to connect them with OMNEXA AI's free strategy consultation at /contact/."
)


def _call_nvidia(conversation_messages: list, api_key: str) -> str | None:
    """Call NVIDIA NIM openai/gpt-oss-120b via OpenAI-compatible endpoint with context history."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_messages
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1500,
        "temperature": 0.7,
    }).encode("utf-8")

    req = urllib.request.Request(
        NVIDIA_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"[GPT-OSS-120B] ❌ HTTP {e.code}: {body[:200]}")
        logger.error(f"NVIDIA HTTP error {e.code}: {body[:200]}")
        return None
    except Exception as e:
        print(f"[GPT-OSS-120B] ❌ Error: {e}")
        logger.error(f"NVIDIA API error: {e}")
        return None


def generate_bot_response(user_message_or_history) -> str:
    """
    Generate a bot response using NVIDIA NIM openai/gpt-oss-120b with full conversation context.
    """
    nvidia_key = (
        os.environ.get("NVIDIA_API_KEY", "")
        or getattr(settings, "NVIDIA_API_KEY", "")
    ).strip()

    if not nvidia_key or not nvidia_key.startswith("nvapi-"):
        print("[GPT-OSS-120B] ❌ No valid NVIDIA API key found.")
        return (
            "I'm having a little trouble connecting right now. "
            "Please try again in a moment, or reach us directly at /contact/ — "
            "we'd love to help! 🙏"
        )

    if isinstance(user_message_or_history, str):
        conversation_messages = [{"role": "user", "content": user_message_or_history}]
    else:
        conversation_messages = user_message_or_history

    reply = _call_nvidia(conversation_messages, nvidia_key)
    if reply:
        print(f"[GPT-OSS-120B ✅] {reply[:80]}...")
        return reply

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

        # Save user message first
        user_msg = ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_message
        )

        # Fetch recent chat context (up to 10 messages)
        recent_msgs = list(session.messages.order_by('-created_at')[:10])[::-1]
        formatted_history = []
        for m in recent_msgs:
            role = 'assistant' if m.role in ('bot', 'assistant') else 'user'
            formatted_history.append({"role": role, "content": m.content})

        # Generate bot response with context
        bot_reply = generate_bot_response(formatted_history)

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
