"""
Utility Classes for LangChain Integration
Professional utility classes for error handling, response formatting, and common operations
"""

import logging
import json
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from django.utils import timezone

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Professional error handling for LangChain operations"""
    
    def __init__(self):
        self.error_count = 0
        self.last_error_time = None
    
    def handle_generation_error(self, error: Exception) -> str:
        """Handle LLM generation errors with graceful fallbacks"""
        self.error_count += 1
        self.last_error_time = timezone.now()
        
        error_type = type(error).__name__
        logger.error(f"❌ Generation Error [{error_type}]: {str(error)}")
        
        # Specific error handling
        if "quota" in str(error).lower() or "limit" in str(error).lower():
            return self._handle_quota_error()
        elif "timeout" in str(error).lower():
            return self._handle_timeout_error()
        elif "authentication" in str(error).lower() or "api_key" in str(error).lower():
            return self._handle_auth_error()
        else:
            return self._handle_generic_error(error)
    
    def handle_interview_error(self, error: Exception) -> Dict[str, Any]:
        """Handle interview-specific errors"""
        logger.error(f"❌ Interview Error: {str(error)}")
        
        return {
            "status": "error",
            "message": "Unable to process interview response at this time",
            "feedback": "Please try again later or contact support",
            "score": None,
            "suggestions": ["Try rephrasing your answer", "Check your internet connection"],
            "error_code": "INTERVIEW_ERROR",
            "timestamp": timezone.now().isoformat()
        }
    
    def handle_chat_error(self, error: Exception) -> str:
        """Handle chat-specific errors"""
        logger.error(f"❌ Chat Error: {str(error)}")
        
        return ("I apologize, but I'm experiencing technical difficulties. "
                "Please try your question again or contact support if the issue persists.")
    
    def handle_analysis_error(self, error: Exception) -> Dict[str, Any]:
        """Handle analysis-specific errors"""
        logger.error(f"❌ Analysis Error: {str(error)}")
        
        return {
            "status": "error",
            "message": "Analysis could not be completed",
            "analysis": None,
            "insights": [],
            "recommendations": ["Please try again later"],
            "error_code": "ANALYSIS_ERROR",
            "timestamp": timezone.now().isoformat()
        }
    
    def _handle_quota_error(self) -> str:
        """Handle API quota exceeded errors"""
        return ("Service temporarily unavailable due to high demand. "
                "Please try again in a few minutes.")
    
    def _handle_timeout_error(self) -> str:
        """Handle timeout errors"""
        return ("Request timed out. Please try again with a shorter prompt "
                "or check your internet connection.")
    
    def _handle_auth_error(self) -> str:
        """Handle authentication errors"""
        return ("Authentication error. Please contact support if this issue persists.")
    
    def _handle_generic_error(self, error: Exception) -> str:
        """Handle generic errors"""
        return (f"An unexpected error occurred. Please try again later. "
                f"Error ID: {hash(str(error)) % 10000}")
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        return {
            "total_errors": self.error_count,
            "last_error": self.last_error_time.isoformat() if self.last_error_time else None,
            "status": "healthy" if self.error_count < 10 else "degraded"
        }


class ResponseFormatter:
    """Professional response formatting and parsing"""
    
    def __init__(self):
        self.format_count = 0
    
    def format_response(self, response: str) -> str:
        """Format and clean general responses"""
        if not response:
            return "No response generated."
        
        # Clean up the response
        formatted = response.strip()
        
        # Remove excessive whitespace
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        formatted = re.sub(r' {2,}', ' ', formatted)
        
        # Ensure proper sentence endings
        if formatted and not formatted.endswith(('.', '!', '?')):
            formatted += '.'
        
        self.format_count += 1
        return formatted
    
    def format_interview_response(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format interview-specific responses with structured output"""
        try:
            # Parse the response for structured data
            feedback_parts = self._parse_interview_feedback(response)
            
            return {
                "status": "success",
                "feedback": feedback_parts.get("feedback", response),
                "score": feedback_parts.get("score", self._extract_score(response)),
                "strengths": feedback_parts.get("strengths", []),
                "improvements": feedback_parts.get("improvements", []),
                "suggestions": feedback_parts.get("suggestions", []),
                "overall_assessment": feedback_parts.get("overall", ""),
                "context": {
                    "role": context.get("role"),
                    "experience": context.get("experience"),
                    "timestamp": timezone.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error formatting interview response: {e}")
            return {
                "status": "partial",
                "feedback": self.format_response(response),
                "score": self._extract_score(response),
                "context": context,
                "timestamp": timezone.now().isoformat()
            }
    
    def format_chat_response(self, response: str) -> str:
        """Format chat responses for optimal display"""
        formatted = self.format_response(response)
        
        # Add professional greeting if response is very short
        if len(formatted) < 20:
            formatted = f"Thank you for your question. {formatted}"
        
        return formatted
    
    def format_analysis_response(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """Format analysis responses with structured output"""
        try:
            analysis_parts = self._parse_analysis_response(response, analysis_type)
            
            return {
                "status": "success",
                "analysis_type": analysis_type,
                "summary": analysis_parts.get("summary", ""),
                "insights": analysis_parts.get("insights", []),
                "recommendations": analysis_parts.get("recommendations", []),
                "metrics": analysis_parts.get("metrics", {}),
                "raw_analysis": response,
                "timestamp": timezone.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error formatting analysis response: {e}")
            return {
                "status": "partial",
                "analysis_type": analysis_type,
                "raw_analysis": self.format_response(response),
                "timestamp": timezone.now().isoformat()
            }
    
    def _parse_interview_feedback(self, response: str) -> Dict[str, Any]:
        """Parse interview feedback into structured components"""
        feedback_parts = {}
        
        # Extract score (looking for patterns like "Score: 8/10" or "8 out of 10")
        score_match = re.search(r'(?:score|rating):\s*(\d+)(?:/10|\s*out\s*of\s*10)', response, re.IGNORECASE)
        if score_match:
            feedback_parts["score"] = int(score_match.group(1))
        
        # Extract sections by common headers
        sections = {
            "strengths": ["strengths", "positives", "good points"],
            "improvements": ["improvements", "areas for improvement", "weaknesses"],
            "suggestions": ["suggestions", "recommendations", "next steps"]
        }
        
        for key, headers in sections.items():
            for header in headers:
                pattern = rf'{header}:?\s*(.*?)(?=\n(?:[A-Z][^:]*:|$))'
                match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    feedback_parts[key] = self._parse_list_items(content)
                    break
        
        return feedback_parts
    
    def _parse_analysis_response(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """Parse analysis response into structured components"""
        analysis_parts = {}
        
        # Extract summary (usually the first paragraph)
        paragraphs = response.split('\n\n')
        if paragraphs:
            analysis_parts["summary"] = paragraphs[0].strip()
        
        # Extract insights and recommendations
        insights_match = re.search(r'insights?:?\s*(.*?)(?=\n(?:[A-Z][^:]*:|$))', response, re.IGNORECASE | re.DOTALL)
        if insights_match:
            analysis_parts["insights"] = self._parse_list_items(insights_match.group(1))
        
        recommendations_match = re.search(r'recommendations?:?\s*(.*?)(?=\n(?:[A-Z][^:]*:|$))', response, re.IGNORECASE | re.DOTALL)
        if recommendations_match:
            analysis_parts["recommendations"] = self._parse_list_items(recommendations_match.group(1))
        
        return analysis_parts
    
    def _parse_list_items(self, text: str) -> List[str]:
        """Parse text into list items"""
        if not text:
            return []
        
        # Split by common list indicators
        items = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                # Remove list indicators
                line = re.sub(r'^[-•*]\s*', '', line)
                line = re.sub(r'^\d+\.\s*', '', line)
                if line:
                    items.append(line)
        
        return items if items else [text.strip()]
    
    def _extract_score(self, text: str) -> Optional[int]:
        """Extract numerical score from text"""
        # Look for score patterns
        patterns = [
            r'(?:score|rating):\s*(\d+)(?:/10)?',
            r'(\d+)\s*(?:out\s*of\s*10|/10)',
            r'(\d+)\s*(?:points?|stars?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return min(max(score, 1), 10)  # Clamp between 1-10
        
        return None
    
    def get_formatting_stats(self) -> Dict[str, Any]:
        """Get formatting statistics"""
        return {
            "total_formatted": self.format_count,
            "status": "active"
        }


class PromptTemplates:
    """Collection of professional prompt templates"""
    
    @staticmethod
    def get_interview_system_prompt(role: str, experience: str, industry: str) -> str:
        """Get system prompt for interview scenarios"""
        return f"""
        You are an expert interview coach and evaluator for Sākṣin, a professional interview platform.
        
        Current Interview Context:
        - Position: {role}
        - Experience Level: {experience}
        - Industry: {industry}
        
        Your role is to:
        1. Provide constructive, professional feedback
        2. Evaluate responses fairly and objectively
        3. Offer specific, actionable improvement suggestions
        4. Maintain an encouraging but honest tone
        5. Consider industry-specific standards and expectations
        
        Structure your feedback with clear sections for strengths, areas for improvement, 
        and specific recommendations. Always provide a score from 1-10 based on the 
        response quality, relevance, and professionalism.
        """
    
    @staticmethod
    def get_analysis_system_prompt(analysis_type: str) -> str:
        """Get system prompt for analysis tasks"""
        prompts = {
            "sentiment": "You are an expert sentiment analyst. Provide detailed sentiment analysis with emotional tone, confidence scores, and key themes.",
            "performance": "You are a performance analyst. Evaluate metrics, identify trends, and provide actionable insights for improvement.",
            "interview": "You are an interview performance analyst. Assess communication skills, technical knowledge, and overall interview performance.",
            "general": "You are a data analyst. Provide comprehensive analysis with clear insights and evidence-based recommendations."
        }
        
        return prompts.get(analysis_type, prompts["general"])
    
    @staticmethod
    def get_chat_system_prompt() -> str:
        """Get system prompt for general chat"""
        return """
        You are a helpful AI assistant for Sākṣin, a professional interview preparation platform.
        
        Guidelines:
        - Provide accurate, helpful information about interviews and career development
        - Be professional but approachable in your tone
        - Offer specific, actionable advice when possible
        - Keep responses concise but comprehensive
        - Ask clarifying questions when needed
        - Maintain user privacy and confidentiality
        
        You can help with interview preparation, career advice, resume tips, 
        technical questions, and general platform guidance.
        """


class ValidationUtils:
    """Utility functions for input validation and sanitization"""
    
    @staticmethod
    def validate_prompt(prompt: str, max_length: int = 10000) -> bool:
        """Validate user prompt input"""
        if not prompt or not isinstance(prompt, str):
            return False
        
        if len(prompt.strip()) == 0:
            return False
        
        if len(prompt) > max_length:
            return False
        
        # Check for potentially harmful content patterns
        harmful_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'eval\s*\(',
            r'exec\s*\('
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return False
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove potentially harmful content
        text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 1000) -> str:
        """Truncate text to specified length with ellipsis"""
        if len(text) <= max_length:
            return text
        
        return text[:max_length-3] + "..."
