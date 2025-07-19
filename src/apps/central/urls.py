"""
URL Configuration for LangChain Central App
Professional URL routing for AI services
"""

from django.urls import path, include
from . import views

app_name = 'central'

# Chat API endpoints
chat_urlpatterns = [
    path('send/', views.ChatAPIView.as_view(), name='chat_send'),
    path('history/', views.ConversationHistoryAPIView.as_view(), name='chat_history'),
]

# Interview API endpoints
interview_urlpatterns = [
    path('start/', views.InterviewSessionAPIView.as_view(), name='interview_start'),
    path('answer/', views.InterviewAnswerAPIView.as_view(), name='interview_answer'),
    path('status/', views.InterviewStatusAPIView.as_view(), name='interview_status'),
]

# Analysis API endpoints
analysis_urlpatterns = [
    path('analyze/', views.AnalysisAPIView.as_view(), name='analysis_analyze'),
]

# Health check endpoints
health_urlpatterns = [
    path('', views.LangChainHealthAPIView.as_view(), name='health_check'),
    path('test/', views.TestAPIView.as_view(), name='test_endpoint'),
]

# Main URL patterns
urlpatterns = [
    # API v1 endpoints (consistent with frontend expectations)
    path('api/v1/chat/', include(chat_urlpatterns)),
    path('api/v1/interview/', include(interview_urlpatterns)),
    path('api/v1/analysis/', include(analysis_urlpatterns)),
    path('api/v1/health/', include(health_urlpatterns)),
    
    # Alternative v1 patterns (without api prefix)
    path('v1/chat/', include(chat_urlpatterns)),
    path('v1/interview/', include(interview_urlpatterns)),
    path('v1/analysis/', include(analysis_urlpatterns)),
    path('v1/health/', include(health_urlpatterns)),
    
    # Direct access patterns (for convenience)
    path('chat/', include(chat_urlpatterns)),
    path('interview/', include(interview_urlpatterns)),
    path('analysis/', include(analysis_urlpatterns)),
    path('health/', include(health_urlpatterns)),
]
