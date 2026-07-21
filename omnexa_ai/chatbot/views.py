"""
Views for chatbot widget backend.
Stores sessions and messages. Integrated with Groq AI for fast, smart responses.
"""

import os
import uuid
import json
import logging
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

# ── Groq AI Setup ─────────────────────────────────────────────────────────────
_groq_client = None

SYSTEM_PROMPT = (
    "You are the OMNEXA AI Assistant — a helpful, friendly, and professional AI chatbot "
    "for OMNEXA AI, a company that specializes in AI-powered business solutions. "
    "Your role is to help visitors learn about OMNEXA AI's services, answer their questions, "
    "and guide them toward booking a free strategy consultation. "
    "\n\nOMNEXA AI services include: AEO (Answer Engine Optimization), AI Marketing, "
    "AI Software Development, AI Chatbots, Content Creation, Image & Video Generation, "
    "Blog Writing, Lead Generation, Meta Ads, Landing Page Optimization, and Social Media Marketing. "
    "\n\nAlways be concise, warm, and end responses with a helpful next step. "
    "If someone asks about pricing, suggest booking a free consultation at /contact/. "
    "Keep responses under 150 words unless the question needs a detailed answer. "
    "Respond in the same language the user is writing in."
)


def _get_groq_client():
    """Lazily initialize and return the Groq client."""
    global _groq_client
    if _groq_client is not None:
        return _groq_client

    api_key = os.environ.get('GROQ_API_KEY', '') or getattr(settings, 'GROQ_API_KEY', '')

    print(f"[GROQ] API key found: {'YES (' + api_key[:8] + '...)' if api_key and api_key != 'your-groq-api-key-here' else 'NO'}")

    if not api_key or api_key == 'your-groq-api-key-here':
        logger.warning("GROQ_API_KEY not set — falling back to rule-based responses.")
        print("[GROQ] WARNING: No API key set, using rule-based fallback.")
        return None

    try:
        from groq import Groq
        _groq_client = Groq(api_key=api_key)
        logger.info("Groq AI client initialized successfully.")
        print("[GROQ] Client initialized successfully!")
        return _groq_client
    except ImportError as e:
        logger.error(f"groq package not installed: {e}")
        print(f"[GROQ] ERROR: groq package not installed: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize Groq AI: {e}")
        print(f"[GROQ] ERROR initializing: {e}")
        return None


def _groq_response(user_message: str) -> str | None:
    """Call Groq API and return the response text, or None on failure."""
    client = _get_groq_client()
    if client is None:
        return None
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        reply = completion.choices[0].message.content.strip()
        print(f"[GROQ] Response OK: {reply[:50]}...")
        return reply
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        print(f"[GROQ] API call ERROR: {e}")
        return None



def generate_bot_response(user_message: str) -> str:
    """
    Generate a bot response.
    First tries Groq AI; falls back to rule-based responses if unavailable.
    """
    # 1️⃣ Try Groq AI first
    ai_reply = _groq_response(user_message)
    if ai_reply:
        return ai_reply

    # 2️⃣ Check knowledge base
    msg = user_message.lower()
    knowledge_responses = ChatbotKnowledgeBase.objects.filter(is_active=True)
    for kb in knowledge_responses:
        keywords = kb.keywords.lower().split(',') if kb.keywords else []
        if any(keyword.strip() in msg for keyword in keywords):
            return kb.answer

    # 3️⃣ Rule-based fallback
    if any(word in msg for word in ['price', 'cost', 'pricing', 'how much', 'charge', 'fee']):
        return ("Our pricing depends on your specific business needs and goals. "
                "Book a free AI strategy call and we'll give you a custom quote. "
                "Click 'Book Free Strategy' in the top menu!")

    if any(word in msg for word in ['aeo', 'answer engine', 'ai search', 'search engine']):
        return ("AEO (Answer Engine Optimization) helps your business appear in AI-powered "
                "search tools like ChatGPT, Perplexity, and Google AI Overviews. "
                "It's the future of SEO. We specialize in this! Want to learn more?")

    if any(word in msg for word in ['chatbot', 'ai bot', 'automation', 'bot']):
        return ("We build AI chatbots that capture leads, answer FAQs, and qualify prospects 24/7 — "
                "even when you're sleeping! Shall I book a free demo for you?")

    if any(word in msg for word in ['lead', 'leads', 'lead generation', 'generate leads']):
        return ("Our AI lead generation systems run 24/7 using chatbots, AI ads, AEO, and automation. "
                "Clients typically see 5X more qualified leads. Want a free strategy session?")

    if any(word in msg for word in ['contact', 'call', 'speak', 'book', 'consultation', 'meeting']):
        return ("I'd love to connect you with our team! "
                "Book your free 30-minute AI strategy call here: /contact/ "
                "No commitment — pure value.")

    if any(word in msg for word in ['service', 'offer', 'provide', 'what do you do']):
        return ("We offer 11 AI-powered services including AEO, AI Marketing, AI Software Development, "
                "AI Chatbots, Content Creation, Image & Video Generation, Blog Writing, Lead Generation, "
                "Meta Ads, Landing Page Optimization, and Social Media Marketing. "
                "Visit /services/ for details!")

    if any(word in msg for word in ['hello', 'hi', 'hey', 'namaste', 'greetings']):
        return ("Hi there! 👋 I'm the OMNEXA AI assistant. "
                "I can help you learn about our AI services, answer your questions, "
                "or book a free strategy call. What can I help you with today?")

    if any(word in msg for word in ['thank', 'thanks', 'appreciate']):
        return ("You're welcome! Is there anything else I can help you with? "
                "Feel free to ask about our services or book a free consultation!")

    if any(word in msg for word in ['bye', 'goodbye', 'see you', 'take care']):
        return ("Goodbye! It was great chatting with you. "
                "Don't forget to book your free AI strategy consultation at /contact/ "
                "We'd love to help transform your business with AI!")

    # Default fallback
    return ("Great question! Our team would love to give you a detailed answer. "
            "Book a free AI strategy consultation at /contact/ and we'll analyze "
            "your business and show you exactly how AI can help you grow. "
            "It's completely free — no commitment!")


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
