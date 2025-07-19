"""
Models for LangChain Integration
Professional models for conversation tracking and session management
"""

from django.db import models
from django.utils import timezone
import uuid
import json

from ..accounts.models import User  # Custom User model from accounts app


class ConversationSession(models.Model):
    """Model to track conversation sessions"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    session_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'central_conversation_sessions'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Conversation {self.id} - {self.user.username}"
    
    @property
    def message_count(self):
        """Get total message count in this conversation"""
        return self.messages.count()
    
    def get_recent_messages(self, limit=10):
        """Get recent messages from this conversation"""
        return self.messages.order_by('-created_at')[:limit]


class ConversationMessage(models.Model):
    """Model to store individual messages in conversations"""
    
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('assistant', 'Assistant Response'),
        ('system', 'System Message'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(ConversationSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'central_conversation_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['message_type']),
        ]
    
    def __str__(self):
        return f"{self.message_type.title()} message in {self.conversation.id}"


class InterviewSession(models.Model):
    """Model to track interview sessions"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    INTERVIEW_TYPES = [
        ('technical', 'Technical Interview'),
        ('behavioral', 'Behavioral Interview'),
        ('coding', 'Coding Interview'),
        ('system_design', 'System Design'),
        ('mixed', 'Mixed Interview'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_sessions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='intermediate')
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    duration_minutes = models.IntegerField(default=45)
    
    # Session tracking
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    current_question_index = models.IntegerField(default=0)
    
    # Configuration and results
    configuration = models.JSONField(default=dict)
    results = models.JSONField(default=dict, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'central_interview_sessions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['interview_type']),
        ]
    
    def __str__(self):
        return f"Interview {self.id} - {self.position} ({self.status})"
    
    @property
    def is_active(self):
        """Check if interview session is currently active"""
        return self.status == 'in_progress'
    
    @property
    def duration_seconds(self):
        """Get actual duration of the interview in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (timezone.now() - self.started_at).total_seconds()
        return 0
    
    def start_session(self):
        """Mark session as started"""
        self.status = 'in_progress'
        self.started_at = timezone.now()
        self.save()
    
    def complete_session(self, results=None):
        """Mark session as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        if results:
            self.results = results
        self.save()


class InterviewQuestion(models.Model):
    """Model to store interview questions and answers"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    answer_text = models.TextField(blank=True)
    question_index = models.IntegerField()
    
    # Timing
    asked_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    
    # Scoring
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    # Metadata
    question_metadata = models.JSONField(default=dict, blank=True)
    answer_metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'central_interview_questions'
        ordering = ['session', 'question_index']
        unique_together = ['session', 'question_index']
        indexes = [
            models.Index(fields=['session', 'question_index']),
        ]
    
    def __str__(self):
        return f"Question {self.question_index + 1} in {self.session.id}"
    
    def submit_answer(self, answer_text, metadata=None):
        """Submit answer for this question"""
        self.answer_text = answer_text
        self.answered_at = timezone.now()
        if self.asked_at:
            self.time_taken_seconds = (self.answered_at - self.asked_at).total_seconds()
        if metadata:
            self.answer_metadata = metadata
        self.save()


class AnalysisRequest(models.Model):
    """Model to track analysis requests"""
    
    ANALYSIS_TYPES = [
        ('general', 'General Analysis'),
        ('sentiment', 'Sentiment Analysis'),
        ('keywords', 'Keyword Extraction'),
        ('summary', 'Text Summary'),
        ('topics', 'Topic Analysis'),
        ('readability', 'Readability Analysis'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis_requests')
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Input data
    input_text = models.TextField()
    input_metadata = models.JSONField(default=dict, blank=True)
    
    # Results
    results = models.JSONField(default=dict, blank=True)
    processing_time_ms = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'central_analysis_requests'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['analysis_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Analysis {self.id} - {self.analysis_type} ({self.status})"
    
    def start_processing(self):
        """Mark analysis as started"""
        self.status = 'processing'
        self.started_at = timezone.now()
        self.save()
    
    def complete_processing(self, results, processing_time_ms=None):
        """Mark analysis as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.results = results
        if processing_time_ms:
            self.processing_time_ms = processing_time_ms
        self.save()
    
    def fail_processing(self, error_message):
        """Mark analysis as failed"""
        self.status = 'failed'
        self.completed_at = timezone.now()
        self.error_message = error_message
        self.save()


class UserFeedback(models.Model):
    """Model to store user feedback on AI responses"""
    
    FEEDBACK_TYPES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('incorrect', 'Incorrect'),
        ('inappropriate', 'Inappropriate'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    
    # Reference to what was rated
    session_id = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100, blank=True)
    
    # Feedback data
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    rating = models.IntegerField(null=True, blank=True)  # 1-5 scale
    comment = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'central_user_feedback'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['feedback_type']),
            models.Index(fields=['processed']),
        ]
    
    def __str__(self):
        return f"Feedback {self.id} - {self.feedback_type}"


class SystemMetrics(models.Model):
    """Model to store system metrics and performance data"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Metrics data
    total_conversations = models.IntegerField(default=0)
    active_sessions = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    avg_response_time_ms = models.FloatField(default=0.0)
    total_tokens_used = models.IntegerField(default=0)
    success_rate = models.FloatField(default=100.0)
    
    # System health
    cpu_usage_percent = models.FloatField(null=True, blank=True)
    memory_usage_percent = models.FloatField(null=True, blank=True)
    disk_usage_percent = models.FloatField(null=True, blank=True)
    
    # Timestamp
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'central_system_metrics'
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['-recorded_at']),
        ]
    
    def __str__(self):
        return f"Metrics {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def get_latest_metrics(cls):
        """Get the most recent metrics"""
        return cls.objects.first()
    
    @classmethod
    def record_metrics(cls, **metrics_data):
        """Record new metrics"""
        return cls.objects.create(**metrics_data)
