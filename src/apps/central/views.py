"""
Django Views for LangChain Integration
Professional API views for chat, interview, and analysis services
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from .langchain_setup.services import ChatService, InterviewService, AnalysisService
from .serializers import (
    ChatMessageSerializer, ChatResponseSerializer,
    InterviewConfigSerializer, InterviewSessionSerializer,
    AnalysisRequestSerializer, AnalysisResponseSerializer
)

logger = logging.getLogger(__name__)


class ChatAPIView(APIView):
    """Professional chat API with conversation management"""
    
    # permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Send a message to the AI chat assistant",
        request_body=ChatMessageSerializer,
        responses={
            200: ChatResponseSerializer,
            400: "Bad Request",
            500: "Internal Server Error"
        },
        tags=['Chat']
    )
    def post(self, request):
        """Send message to chat service"""
        try:
            serializer = ChatMessageSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid request data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            chat_service = ChatService()
            
            # Extract data
            message = serializer.validated_data['message']
            conversation_id = serializer.validated_data.get('conversation_id', None)
            user_id = str(request.user.id)
            
            # Send message
            response_data = chat_service.send_message(
                message=message,
                user_id=user_id,
                conversation_id=conversation_id
            )
            
            if response_data['status'] == 'success':
                response_serializer = ChatResponseSerializer(data=response_data)
                if response_serializer.is_valid():
                    return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
                else:
                    return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"❌ Error in chat API: {e}")
            return Response(
                {"error": "Internal server error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ConversationHistoryAPIView(APIView):
    """Get conversation history for a user"""
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get conversation history",
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_QUERY,
                description="Conversation ID",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: "Conversation history", 404: "Not found"},
        tags=['Chat']
    )
    def get(self, request):
        """Get conversation history"""
        try:
            conversation_id = request.query_params.get('conversation_id')
            if not conversation_id:
                return Response(
                    {"error": "conversation_id parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            chat_service = ChatService()
            user_id = str(request.user.id)
            
            history = chat_service.get_conversation_history(conversation_id, user_id)
            
            return Response({
                "conversation_id": conversation_id,
                "history": history,
                "message_count": len(history)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"❌ Error getting conversation history: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InterviewSessionAPIView(APIView):
    """Start and manage interview sessions"""
    
    # Temporarily commented out for testing
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Start a new interview session",
        request_body=InterviewConfigSerializer,
        responses={
            201: InterviewSessionSerializer,
            400: "Bad Request",
            500: "Internal Server Error"
        },
        tags=['Interview']
    )
    def post(self, request):
        """Start new interview session"""
        try:
            data = request.data.copy()  # Ensures mutable dict in Django or FastAPI
            position = data.get("position")
            role = data.get("role")
            # Debug logging
            logger.info(f"📝 Received interview start request")
            
            if position:
                data["role"] = position
                logger.info(f"🔄 Overwriting 'role' with 'position': {position}")
            # request.data = data  # Update request data
            logger.info(f"📝 Request data: {data}")
            logger.info(f"📝 User authenticated: {request.user.is_authenticated if hasattr(request, 'user') else 'No user'}")
            
            serializer = InterviewConfigSerializer(data=data)
            if not serializer.is_valid():
                logger.error(f"❌ Serializer validation failed: {serializer.errors}")
                return Response(
                    {"error": "Invalid configuration", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            interview_service = InterviewService()
            # Handle both authenticated and non-authenticated requests
            if hasattr(request, 'user') and request.user.is_authenticated:
                user_id = str(request.user.id)
            else:
                user_id = "anonymous_user"  # Temporary for testing
            
            # Start session
            session_data = interview_service.start_interview_session(
                user_id=user_id,
                interview_config=serializer.validated_data
            )
            
            if session_data['status'] == 'success':
                return Response(session_data, status=status.HTTP_201_CREATED)
            else:
                return Response(session_data, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"❌ Error starting interview session: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InterviewAnswerAPIView(APIView):
    """Submit interview answers"""
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Submit an answer to interview question",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'session_id': openapi.Schema(type=openapi.TYPE_STRING),
                'answer': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['session_id', 'answer']
        ),
        responses={200: "Answer processed", 400: "Bad Request"},
        tags=['Interview']
    )
    def post(self, request):
        """Submit interview answer"""
        try:
            session_id = request.data.get('session_id')
            answer = request.data.get('answer')
            
            if not session_id or not answer:
                return Response(
                    {"error": "session_id and answer are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            interview_service = InterviewService()
            
            # Submit answer
            result = interview_service.submit_answer(session_id, answer)
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"❌ Error submitting interview answer: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InterviewStatusAPIView(APIView):
    """Get interview session status"""
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get interview session status",
        manual_parameters=[
            openapi.Parameter(
                'session_id',
                openapi.IN_QUERY,
                description="Interview session ID",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: "Session status", 404: "Not found"},
        tags=['Interview']
    )
    def get(self, request):
        """Get interview session status"""
        try:
            session_id = request.query_params.get('session_id')
            if not session_id:
                return Response(
                    {"error": "session_id parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            interview_service = InterviewService()
            status_data = interview_service.get_session_status(session_id)
            
            return Response(status_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"❌ Error getting interview status: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnalysisAPIView(APIView):
    """Analysis service endpoints"""
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Perform text analysis",
        request_body=AnalysisRequestSerializer,
        responses={
            200: AnalysisResponseSerializer,
            400: "Bad Request",
            500: "Internal Server Error"
        },
        tags=['Analysis']
    )
    def post(self, request):
        """Perform analysis on provided data"""
        try:
            serializer = AnalysisRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "Invalid request data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            analysis_service = AnalysisService()
            user_id = str(request.user.id)
            
            # Extract data
            text = serializer.validated_data['text']
            analysis_type = serializer.validated_data.get('analysis_type', 'general')
            
            # Perform analysis based on type
            if analysis_type == 'sentiment':
                result = analysis_service.analyze_sentiment(text, user_id)
            else:
                # For other types, use general analysis
                from .langchain_setup.clients import ClientFactory
                client = ClientFactory.get_default_client()
                result = client.generate_analysis(text, analysis_type)
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"❌ Error in analysis API: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LangChainHealthAPIView(APIView):
    """Health check endpoint for LangChain services"""
    
    @swagger_auto_schema(
        operation_description="Check health status of LangChain services",
        responses={200: "Service status"},
        tags=['Health']
    )
    def get(self, request):
        """Get health status of all LangChain services"""
        try:
            from .langchain_setup.config import LangChainConfig
            from .langchain_setup.clients import ClientFactory
            
            health_status = {
                "status": "healthy",
                "timestamp": "2025-01-18T00:00:00Z",
                "services": {}
            }
            
            # Check configuration
            try:
                LangChainConfig.validate_config()
                health_status["services"]["configuration"] = "healthy"
            except Exception as e:
                health_status["services"]["configuration"] = f"error: {str(e)}"
                health_status["status"] = "degraded"
            
            # Check client
            try:
                ClientFactory.get_default_client()
                health_status["services"]["gemini_client"] = "healthy"
            except Exception as e:
                health_status["services"]["gemini_client"] = f"error: {str(e)}"
                health_status["status"] = "degraded"
            
            # Check services
            try:
                ChatService()
                health_status["services"]["chat_service"] = "healthy"
            except Exception as e:
                health_status["services"]["chat_service"] = f"error: {str(e)}"
                health_status["status"] = "degraded"
            
            try:
                InterviewService()
                health_status["services"]["interview_service"] = "healthy"
            except Exception as e:
                health_status["services"]["interview_service"] = f"error: {str(e)}"
                health_status["status"] = "degraded"
            
            try:
                AnalysisService()
                health_status["services"]["analysis_service"] = "healthy"
            except Exception as e:
                health_status["services"]["analysis_service"] = f"error: {str(e)}"
                health_status["status"] = "degraded"
            
            return Response(health_status, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"❌ Error in health check: {e}")
            return Response({
                "status": "error",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestAPIView(APIView):
    """Simple test endpoint to verify routing and authentication"""
    
    def get(self, request):
        """Test endpoint"""
        return Response({
            "message": "API is working",
            "authenticated": request.user.is_authenticated if hasattr(request, 'user') else False,
            "user_id": str(request.user.id) if hasattr(request, 'user') and request.user.is_authenticated else None,
            "timestamp": "2025-07-19T00:00:00Z"
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Test POST endpoint"""
        return Response({
            "message": "POST request received",
            "data_received": request.data,
            "authenticated": request.user.is_authenticated if hasattr(request, 'user') else False,
            "user_id": str(request.user.id) if hasattr(request, 'user') and request.user.is_authenticated else None,
        }, status=status.HTTP_200_OK)
