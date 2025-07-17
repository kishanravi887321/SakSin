from django.db import models
from ..accounts.models import User  # Adjust this import to match your project structure

class Analytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics')
    session_id = models.CharField(max_length=255, blank=True, null=True)
    page_viewed = models.CharField(max_length=255, blank=True, null=True)
    action_performed = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True, help_text="Duration in seconds")
    device_type = models.CharField(max_length=50, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Analytics"
        verbose_name_plural = "Analytics"
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user.email} - {self.page_viewed} - {self.timestamp}"