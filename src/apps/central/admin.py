"""
Django Admin Configuration for LangChain Central App
Professional admin interface for AI service management
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
import json

from .models import (
    ConversationSession, ConversationMessage, InterviewSession,
    InterviewQuestion, AnalysisRequest, UserFeedback, SystemMetrics
)


@admin.register(ConversationSession)
class ConversationSessionAdmin(admin.ModelAdmin):
    """Admin interface for conversation sessions"""
    
    list_display = ['id', 'user', 'title', 'message_count', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at', 'message_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'title', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Session Data', {
            'fields': ('session_data', 'message_count'),
            'classes': ('collapse',)
        }),
    )
    
    def message_count(self, obj):
        """Display message count"""
        count = obj.message_count
        if count > 0:
            url = reverse('admin:central_conversationmessage_changelist')
            return format_html(
                '<a href="{}?conversation__id__exact={}">{} messages</a>',
                url, obj.id, count
            )
        return '0 messages'
    message_count.short_description = 'Messages'


class ConversationMessageInline(admin.TabularInline):
    """Inline for conversation messages"""
    model = ConversationMessage
    extra = 0
    readonly_fields = ['id', 'created_at', 'tokens_used']
    fields = ['message_type', 'content', 'tokens_used', 'created_at']
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    """Admin interface for conversation messages"""
    
    list_display = ['id', 'conversation', 'message_type', 'content_preview', 'tokens_used', 'created_at']
    list_filter = ['message_type', 'created_at']
    search_fields = ['conversation__user__username', 'content']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('id', 'conversation', 'message_type', 'content')
        }),
        ('Metadata', {
            'fields': ('tokens_used', 'metadata', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        """Show content preview"""
        if len(obj.content) > 100:
            return f"{obj.content[:100]}..."
        return obj.content
    content_preview.short_description = 'Content Preview'


class InterviewQuestionInline(admin.TabularInline):
    """Inline for interview questions"""
    model = InterviewQuestion
    extra = 0
    readonly_fields = ['id', 'asked_at', 'answered_at', 'time_taken_seconds']
    fields = ['question_index', 'question_text', 'answer_text', 'score', 'time_taken_seconds']


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    """Admin interface for interview sessions"""
    
    list_display = [
        'id', 'user', 'position', 'interview_type', 'difficulty', 
        'status', 'overall_score', 'duration_display', 'created_at'
    ]
    list_filter = ['status', 'interview_type', 'difficulty', 'created_at']
    search_fields = ['user__username', 'position', 'company']
    readonly_fields = ['id', 'created_at', 'updated_at', 'duration_seconds']
    date_hierarchy = 'created_at'
    inlines = [InterviewQuestionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'status', 'position', 'company')
        }),
        ('Interview Configuration', {
            'fields': ('interview_type', 'difficulty', 'duration_minutes', 'configuration')
        }),
        ('Session Tracking', {
            'fields': ('started_at', 'completed_at', 'current_question_index', 'duration_seconds'),
            'classes': ('collapse',)
        }),
        ('Results', {
            'fields': ('overall_score', 'results'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_display(self, obj):
        """Display formatted duration"""
        seconds = obj.duration_seconds
        if seconds > 0:
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}m {remaining_seconds}s"
        return "Not started"
    duration_display.short_description = 'Duration'


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    """Admin interface for interview questions"""
    
    list_display = [
        'id', 'session', 'question_index', 'question_preview', 
        'answered', 'score', 'time_taken_seconds'
    ]
    list_filter = ['session__interview_type', 'session__difficulty']
    search_fields = ['session__user__username', 'question_text', 'answer_text']
    readonly_fields = ['id', 'asked_at', 'answered_at', 'time_taken_seconds']
    
    fieldsets = (
        ('Question Information', {
            'fields': ('id', 'session', 'question_index', 'question_text')
        }),
        ('Answer Information', {
            'fields': ('answer_text', 'answered_at', 'time_taken_seconds')
        }),
        ('Evaluation', {
            'fields': ('score', 'feedback')
        }),
        ('Metadata', {
            'fields': ('question_metadata', 'answer_metadata', 'asked_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        """Show question preview"""
        if len(obj.question_text) > 80:
            return f"{obj.question_text[:80]}..."
        return obj.question_text
    question_preview.short_description = 'Question'
    
    def answered(self, obj):
        """Show if question is answered"""
        return bool(obj.answer_text)
    answered.boolean = True


@admin.register(AnalysisRequest)
class AnalysisRequestAdmin(admin.ModelAdmin):
    """Admin interface for analysis requests"""
    
    list_display = [
        'id', 'user', 'analysis_type', 'status', 
        'processing_time_ms', 'created_at'
    ]
    list_filter = ['analysis_type', 'status', 'created_at']
    search_fields = ['user__username', 'input_text']
    readonly_fields = ['id', 'created_at', 'started_at', 'completed_at', 'processing_time_ms']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('id', 'user', 'analysis_type', 'status')
        }),
        ('Input Data', {
            'fields': ('input_text', 'input_metadata')
        }),
        ('Results', {
            'fields': ('results', 'processing_time_ms', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    """Admin interface for user feedback"""
    
    list_display = [
        'id', 'user', 'feedback_type', 'rating', 
        'session_id', 'processed', 'created_at'
    ]
    list_filter = ['feedback_type', 'rating', 'processed', 'created_at']
    search_fields = ['user__username', 'session_id', 'comment']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('id', 'user', 'session_id', 'message_id')
        }),
        ('Feedback Data', {
            'fields': ('feedback_type', 'rating', 'comment')
        }),
        ('Processing', {
            'fields': ('processed', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    
    def mark_as_processed(self, request, queryset):
        """Mark feedback as processed"""
        updated = queryset.update(processed=True)
        self.message_user(request, f'{updated} feedback items marked as processed.')
    mark_as_processed.short_description = 'Mark selected feedback as processed'
    
    def mark_as_unprocessed(self, request, queryset):
        """Mark feedback as unprocessed"""
        updated = queryset.update(processed=False)
        self.message_user(request, f'{updated} feedback items marked as unprocessed.')
    mark_as_unprocessed.short_description = 'Mark selected feedback as unprocessed'


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    """Admin interface for system metrics"""
    
    list_display = [
        'id', 'total_conversations', 'active_sessions', 'total_messages',
        'avg_response_time_ms', 'success_rate', 'recorded_at'
    ]
    list_filter = ['recorded_at']
    readonly_fields = [
        'id', 'total_conversations', 'active_sessions', 'total_messages',
        'avg_response_time_ms', 'total_tokens_used', 'success_rate',
        'cpu_usage_percent', 'memory_usage_percent', 'disk_usage_percent',
        'recorded_at'
    ]
    date_hierarchy = 'recorded_at'
    
    fieldsets = (
        ('Usage Metrics', {
            'fields': (
                'total_conversations', 'active_sessions', 'total_messages',
                'avg_response_time_ms', 'total_tokens_used', 'success_rate'
            )
        }),
        ('System Health', {
            'fields': ('cpu_usage_percent', 'memory_usage_percent', 'disk_usage_percent'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual addition of metrics"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing of metrics"""
        return False


# Custom admin site configuration
admin.site.site_header = 'SakSIn LangChain Administration'
admin.site.site_title = 'SakSIn Admin'
admin.site.index_title = 'LangChain Management Dashboard'
