"""
Serializers for LangChain Integration
Professional serializers for chat, interview, and analysis services
"""

from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator


class ChatMessageSerializer(serializers.Serializer):
    """Serializer for chat message requests"""
    
    message = serializers.CharField(
        max_length=2000,
        validators=[MinLengthValidator(1)],
        help_text="The message to send to the AI assistant"
    )
    conversation_id = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        help_text="Optional conversation ID to continue existing conversation"
    )
    context = serializers.DictField(
        required=False,
        allow_null=True,
        help_text="Optional context data for the conversation"
    )
    
    def validate_message(self, value):
        """Validate message content"""
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value.strip()


class ChatResponseSerializer(serializers.Serializer):
    """Serializer for chat response data"""
    
    status = serializers.CharField()
    response = serializers.CharField()
    conversation_id = serializers.CharField()
    message_id = serializers.CharField()
    timestamp = serializers.DateTimeField()
    tokens_used = serializers.IntegerField(required=False)
    
    class Meta:
        fields = ['status', 'response', 'conversation_id', 'message_id', 'timestamp', 'tokens_used']


class InterviewConfigSerializer(serializers.Serializer):
    """Serializer for interview configuration"""
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ]
    
    INTERVIEW_TYPES = [
        ('technical', 'Technical Interview'),
        ('behavioral', 'Behavioral Interview'),
        ('coding', 'Coding Interview'),
        ('system_design', 'System Design'),
        ('mixed', 'Mixed Interview')
    ]
    
    interview_type = serializers.ChoiceField(
        choices=INTERVIEW_TYPES,
        help_text="Type of interview to conduct"
    )
    difficulty = serializers.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        default='intermediate',
        help_text="Difficulty level of the interview"
    )
    duration_minutes = serializers.IntegerField(
        min_value=15,
        max_value=180,
        default=45,
        help_text="Interview duration in minutes"
    )
    # Changed to match frontend and service expectations
    role = serializers.CharField(
        max_length=200,
        help_text="Role/Position being interviewed for"
    )
    experience = serializers.CharField(
        max_length=200,
        help_text="Experience level (e.g., '3 years', 'Senior', etc.)"
    )
    industry = serializers.CharField(
        max_length=200,
        help_text="Industry (e.g., 'Technology', 'Finance', etc.)"
    )
    position = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Specific position title (optional)"
    )
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        help_text="List of skills to focus on"
    )
    custom_questions = serializers.ListField(
        child=serializers.CharField(max_length=500),
        required=False,
        help_text="Custom questions to include"
    )
   
    experience = serializers.CharField(
        max_length=100,
        required=False,
        default='Mid-level',
        help_text="Experience level of the candidate (e.g., Junior, Mid-level, Senior)"
    )
    print('all p[ass]')
    
    def validate_skills(self, value):
        """Validate skills list"""
        if value and len(value) > 10:
            raise serializers.ValidationError("Maximum 10 skills allowed")
        return value
    
    def validate_custom_questions(self, value):
        """Validate custom questions"""
        if value and len(value) > 5:
            raise serializers.ValidationError("Maximum 5 custom questions allowed")
        return value


class InterviewSessionSerializer(serializers.Serializer):
    """Serializer for interview session data"""
    
    status = serializers.CharField()
    session_id = serializers.CharField()
    interview_config = InterviewConfigSerializer()
    current_question = serializers.CharField(required=False)
    question_number = serializers.IntegerField(required=False)
    total_questions = serializers.IntegerField(required=False)
    start_time = serializers.DateTimeField()
    estimated_end_time = serializers.DateTimeField()
    
    class Meta:
        fields = [
            'status', 'session_id', 'interview_config', 'current_question',
            'question_number', 'total_questions', 'start_time', 'estimated_end_time'
        ]


class InterviewAnswerSerializer(serializers.Serializer):
    """Serializer for interview answer submission"""
    
    session_id = serializers.CharField(
        max_length=100,
        help_text="Interview session ID"
    )
    answer = serializers.CharField(
        max_length=5000,
        validators=[MinLengthValidator(10)],
        help_text="Interview answer"
    )
    time_taken_seconds = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text="Time taken to answer in seconds"
    )
    
    def validate_answer(self, value):
        """Validate answer content"""
        if not value.strip():
            raise serializers.ValidationError("Answer cannot be empty")
        return value.strip()


class AnalysisRequestSerializer(serializers.Serializer):
    """Serializer for analysis requests"""
    
    ANALYSIS_TYPES = [
        ('general', 'General Analysis'),
        ('sentiment', 'Sentiment Analysis'),
        ('keywords', 'Keyword Extraction'),
        ('summary', 'Text Summary'),
        ('topics', 'Topic Analysis'),
        ('readability', 'Readability Analysis')
    ]
    
    text = serializers.CharField(
        max_length=10000,
        validators=[MinLengthValidator(10)],
        help_text="Text to analyze"
    )
    analysis_type = serializers.ChoiceField(
        choices=ANALYSIS_TYPES,
        default='general',
        help_text="Type of analysis to perform"
    )
    language = serializers.CharField(
        max_length=10,
        default='en',
        help_text="Language code (e.g., 'en', 'es', 'fr')"
    )
    options = serializers.DictField(
        required=False,
        help_text="Additional options for analysis"
    )
    
    def validate_text(self, value):
        """Validate text content"""
        if not value.strip():
            raise serializers.ValidationError("Text cannot be empty")
        return value.strip()


class AnalysisResponseSerializer(serializers.Serializer):
    """Serializer for analysis response data"""
    
    status = serializers.CharField()
    analysis_type = serializers.CharField()
    results = serializers.DictField()
    metadata = serializers.DictField(required=False)
    timestamp = serializers.DateTimeField()
    processing_time_ms = serializers.IntegerField(required=False)
    
    class Meta:
        fields = ['status', 'analysis_type', 'results', 'metadata', 'timestamp', 'processing_time_ms']


class ConversationHistorySerializer(serializers.Serializer):
    """Serializer for conversation history"""
    
    conversation_id = serializers.CharField()
    messages = serializers.ListField(
        child=serializers.DictField()
    )
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    message_count = serializers.IntegerField()
    
    class Meta:
        fields = ['conversation_id', 'messages', 'created_at', 'updated_at', 'message_count']


class InterviewReportSerializer(serializers.Serializer):
    """Serializer for interview completion report"""
    
    session_id = serializers.CharField()
    overall_score = serializers.FloatField(min_value=0, max_value=100)
    detailed_scores = serializers.DictField()
    strengths = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    areas_for_improvement = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    recommendations = serializers.ListField(
        child=serializers.CharField(max_length=300)
    )
    duration_minutes = serializers.IntegerField()
    questions_answered = serializers.IntegerField()
    
    class Meta:
        fields = [
            'session_id', 'overall_score', 'detailed_scores', 'strengths',
            'areas_for_improvement', 'recommendations', 'duration_minutes', 'questions_answered'
        ]


class FeedbackSerializer(serializers.Serializer):
    """Serializer for user feedback on AI responses"""
    
    FEEDBACK_TYPES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('incorrect', 'Incorrect'),
        ('inappropriate', 'Inappropriate')
    ]
    
    session_id = serializers.CharField(max_length=100)
    message_id = serializers.CharField(max_length=100)
    feedback_type = serializers.ChoiceField(choices=FEEDBACK_TYPES)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    comment = serializers.CharField(max_length=500, required=False)
    
    def validate(self, data):
        """Validate feedback data"""
        if data['feedback_type'] in ['not_helpful', 'incorrect'] and not data.get('comment'):
            raise serializers.ValidationError(
                "Comment is required for negative feedback"
            )
        return data


class SystemMetricsSerializer(serializers.Serializer):
    """Serializer for system metrics and health data"""
    
    total_conversations = serializers.IntegerField()
    active_sessions = serializers.IntegerField()
    avg_response_time_ms = serializers.FloatField()
    total_tokens_used = serializers.IntegerField()
    success_rate = serializers.FloatField(min_value=0, max_value=100)
    uptime_hours = serializers.FloatField()
    
    class Meta:
        fields = [
            'total_conversations', 'active_sessions', 'avg_response_time_ms',
            'total_tokens_used', 'success_rate', 'uptime_hours'
        ]
