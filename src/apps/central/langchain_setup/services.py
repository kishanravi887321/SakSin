"""
Professional Service Classes for LangChain Integration
High-level service classes that combine clients and utilities for specific use cases
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.cache import cache

from .clients import GeminiClient, ClientFactory
# from .clients import OllamaClient, ClientFactory
from .utils import ErrorHandler, ResponseFormatter, PromptTemplates, ValidationUtils
from .config import LangChainConfig

logger = logging.getLogger(__name__)


class BaseService:
    """Base service class with common functionality"""
    
    def __init__(self):
        self.client = ClientFactory.get_default_client()
        self.error_handler = ErrorHandler()
        self.formatter = ResponseFormatter()
        self.validator = ValidationUtils()
        self.config = LangChainConfig()
    
    def _get_cache_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key for storing responses"""
        return f"langchain:{prefix}:{hash(identifier)}"
    
    def _cache_response(self, key: str, response: Any, ttl: int = None) -> None:
        """Cache response with TTL"""
        if self.config.CACHE_ENABLED:
            cache.set(key, response, ttl or self.config.CACHE_TTL)
    
    def _get_cached_response(self, key: str) -> Optional[Any]:
        """Retrieve cached response"""
        if self.config.CACHE_ENABLED:
            return cache.get(key)
        return None


class ChatService(BaseService):
    """Professional chat service for conversational AI interactions"""
    
    def __init__(self):
        super().__init__()
        self.conversation_cache = {}
        self.rate_limiter = {}
    
    def send_message(self, message: str, user_id: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Send a message and get AI response
        
        Args:
            message: User message
            user_id: User identifier
            conversation_id: Optional conversation identifier
            
        Returns:
            Response dictionary with message and metadata
        """
        try:
            # Validate input
            if not self.validator.validate_prompt(message):
                return {
                    "status": "error",
                    "message": "Invalid message format",
                    "response": None
                }
            
            # Check rate limiting
            if not self._check_rate_limit(user_id):
                return {
                    "status": "error", 
                    "message": "Rate limit exceeded. Please wait before sending another message.",
                    "response": None
                }
            
            # Sanitize input
            clean_message = self.validator.sanitize_input(message)
            
            # Get conversation history
            conversation_history = self._get_conversation_history(conversation_id, user_id)
            
            # Check cache for similar recent messages
            cache_key = self._get_cache_key("chat", f"{user_id}:{clean_message}")
            cached_response = self._get_cached_response(cache_key)
            
            if cached_response:
                logger.info(f"✅ Returning cached chat response for user {user_id}")
                return cached_response
            
            # Generate response
            response_text = self.client.generate_chat_response(
                message=clean_message,
                conversation_history=conversation_history
            )
            
            # Format response
            response_data = {
                "status": "success",
                "message": clean_message,
                "response": response_text,
                "conversation_id": conversation_id or self._generate_conversation_id(user_id),
                "timestamp": timezone.now().isoformat(),
                "metadata": {
                    "user_id": user_id,
                    "message_length": len(clean_message),
                    "response_length": len(response_text)
                }
            }
            
            # Cache response
            self._cache_response(cache_key, response_data)
            
            # Update conversation history
            self._update_conversation_history(
                conversation_id or response_data["conversation_id"],
                user_id,
                clean_message,
                response_text
            )
            
            # Update rate limiter
            self._update_rate_limit(user_id)
            
            logger.info(f"✅ Chat response generated for user {user_id}")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error in chat service: {e}")
            return {
                "status": "error",
                "message": "Service temporarily unavailable",
                "response": self.error_handler.handle_chat_error(e),
                "timestamp": timezone.now().isoformat()
            }
    
    def get_conversation_history(self, conversation_id: str, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a user"""
        return self._get_conversation_history(conversation_id, user_id)
    
    def clear_conversation(self, conversation_id: str, user_id: str) -> bool:
        """Clear conversation history"""
        try:
            cache_key = f"conversation:{conversation_id}:{user_id}"
            cache.delete(cache_key)
            return True
        except Exception as e:
            logger.error(f"❌ Error clearing conversation: {e}")
            return False
    
    def _check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limits"""
        now = timezone.now()
        user_requests = self.rate_limiter.get(user_id, [])
        
        # Remove old requests (older than 1 hour)
        user_requests = [req_time for req_time in user_requests 
                        if now - req_time < timedelta(hours=1)]
        
        # Check limits
        recent_requests = [req_time for req_time in user_requests 
                          if now - req_time < timedelta(minutes=1)]
        
        if len(recent_requests) >= self.config.MAX_REQUESTS_PER_MINUTE:
            return False
        
        if len(user_requests) >= self.config.MAX_REQUESTS_PER_HOUR:
            return False
        
        return True
    
    def _update_rate_limit(self, user_id: str) -> None:
        """Update rate limit tracking for user"""
        now = timezone.now()
        if user_id not in self.rate_limiter:
            self.rate_limiter[user_id] = []
        
        self.rate_limiter[user_id].append(now)
        
        # Keep only recent requests
        self.rate_limiter[user_id] = [
            req_time for req_time in self.rate_limiter[user_id]
            if now - req_time < timedelta(hours=1)
        ]
    
    def _generate_conversation_id(self, user_id: str) -> str:
        """Generate unique conversation ID"""
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        return f"conv_{user_id}_{timestamp}"
    
    def _get_conversation_history(self, conversation_id: str, user_id: str) -> List[Dict[str, Any]]:
        """Get conversation history from cache"""
        if not conversation_id:
            return []
        
        cache_key = f"conversation:{conversation_id}:{user_id}"
        history = cache.get(cache_key, [])
        return history[-10:]  # Return last 10 messages
    
    def _update_conversation_history(self, conversation_id: str, user_id: str, 
                                   user_message: str, ai_response: str) -> None:
        """Update conversation history in cache"""
        cache_key = f"conversation:{conversation_id}:{user_id}"
        history = cache.get(cache_key, [])
        
        # Add new messages
        history.extend([
            {
                "role": "user",
                "content": user_message,
                "timestamp": timezone.now().isoformat()
            },
            {
                "role": "assistant", 
                "content": ai_response,
                "timestamp": timezone.now().isoformat()
            }
        ])
        
        # Keep only recent messages (last 20)
        history = history[-20:]
        
        # Cache updated history
        cache.set(cache_key, history, 3600)  # 1 hour


class InterviewService(BaseService):
    """Professional interview service for AI-powered interview simulations"""
    
    def __init__(self):
        super().__init__()
        self.active_sessions = {}
    
    def start_interview_session(self, user_id: str, interview_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a new interview session
        
        Args:
            user_id: User identifier
            interview_config: Configuration including role, experience, industry
            
        Returns:
            Session details and first question
        """
        try:
            # Validate configuration
            required_fields = ['role', 'experience', 'industry']
            for field in required_fields:
                if field not in interview_config:
                    return {
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }
            
            # Generate session ID
            session_id = f"interview_{user_id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Initialize session data
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "config": interview_config,
                "questions": [],
                "responses": [],
                "start_time": timezone.now().isoformat(),
                "status": "active",
                "current_question_index": 0
            }
            
            # Generate first question
            first_question = self._generate_interview_question(
                session_data, 
                question_number=1
            )
            
            if not first_question:
                logger.error("❌ Failed to generate first interview question")
                return {
                    "status": "error",
                    "message": "Unable to generate interview questions"
                }
            
            session_data["questions"].append(first_question)
            
            # Add debug logging
            logger.info(f"📊 Session initialized with {len(session_data['questions'])} questions")
            logger.info(f"📊 Current question index: {session_data['current_question_index']}")
            
            # Cache session
            cache.set(f"interview_session:{session_id}", session_data, 
                     self.config.INTERVIEW_SESSION_TIMEOUT)
            
            logger.info(f"✅ Interview session started: {session_id}")
            
            return {
                "status": "success",
                "session_id": session_id,
                "question": first_question,
                "session_info": {
                    "role": interview_config["role"],
                    "experience": interview_config["experience"],
                    "industry": interview_config["industry"],
                    "question_number": 1,
                    "total_questions": self.config.MAX_INTERVIEW_QUESTIONS
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error starting interview session: {e}")
            return {
                "status": "error",
                "message": "Unable to start interview session",
                "error": str(e)
            }
    
    def submit_answer(self, session_id: str, answer: str) -> Dict[str, Any]:
        """
        Submit an answer and get feedback + next question
        
        Args:
            session_id: Interview session identifier
            answer: User's answer to current question
            
        Returns:
            Feedback and next question or session completion
        """
        try:
            # Get session data
            session_data = cache.get(f"interview_session:{session_id}")
            if not session_data:
                return {
                    "status": "error",
                    "message": "Interview session not found or expired"
                }
            
            # Validate and repair session data
            session_data = self._validate_and_repair_session(session_data)
            
            # Add debug logging
            logger.info(f"📊 Processing answer for session {session_id}")
            logger.info(f"📊 Current question index: {session_data.get('current_question_index', 'Not set')}")
            logger.info(f"📊 Total questions available: {len(session_data.get('questions', []))}")
            
            # Validate answer
            if not self.validator.validate_prompt(answer):
                return {
                    "status": "error",
                    "message": "Invalid answer format"
                }
            
            # Sanitize answer
            clean_answer = self.validator.sanitize_input(answer)
            
            # Get current question - ensure index is valid
            current_question_index = session_data["current_question_index"]
            if current_question_index >= len(session_data["questions"]):
                return {
                    "status": "error",
                    "message": "Invalid question index - session may be corrupted"
                }
            
            current_question = session_data["questions"][current_question_index]
            
            # Generate feedback
            feedback = self.client.generate_interview_response(
                question=f"Question: {current_question}\nAnswer: {clean_answer}",
                context=session_data["config"]
            )
            
            # Store response
            response_data = {
                "question": current_question,
                "answer": clean_answer,
                "feedback": feedback,
                "timestamp": timezone.now().isoformat(),
                "question_number": current_question_index + 1
            }
            
            session_data["responses"].append(response_data)
            
            # Move to next question
            next_question_index = current_question_index + 1
            
            # Check if interview should continue
            if (next_question_index >= self.config.MAX_INTERVIEW_QUESTIONS):
                
                # End interview
                session_data["status"] = "completed"
                session_data["end_time"] = timezone.now().isoformat()
                session_data["current_question_index"] = next_question_index
                
                # Generate final summary
                final_summary = self._generate_interview_summary(session_data)
                
                # Update cache
                cache.set(f"interview_session:{session_id}", session_data, 
                         self.config.INTERVIEW_SESSION_TIMEOUT)
                
                return {
                    "status": "completed",
                    "session_id": session_id,
                    "feedback": feedback,
                    "final_summary": final_summary,
                    "total_questions": len(session_data["responses"])
                }
            
            else:
                # Generate next question
                next_question = self._generate_interview_question(
                    session_data,
                    question_number=next_question_index + 1
                )
                
                session_data["questions"].append(next_question)
                session_data["current_question_index"] = next_question_index
                
                # Update cache
                cache.set(f"interview_session:{session_id}", session_data,
                         self.config.INTERVIEW_SESSION_TIMEOUT)
                
                return {
                    "status": "continue",
                    "session_id": session_id,
                    "feedback": feedback,
                    "next_question": next_question,
                    "progress": {
                        "current_question": next_question_index + 1,
                        "total_questions": self.config.MAX_INTERVIEW_QUESTIONS
                    }
                }
            
        except Exception as e:
            logger.error(f"❌ Error submitting interview answer: {e}")
            return {
                "status": "error",
                "message": "Unable to process answer",
                "feedback": self.error_handler.handle_interview_error(e)
            }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current session status and progress"""
        try:
            session_data = cache.get(f"interview_session:{session_id}")
            if not session_data:
                return {
                    "status": "not_found",
                    "message": "Session not found or expired"
                }
            
            # Validate and repair session data if needed
            session_data = self._validate_and_repair_session(session_data)
            
            # Add detailed diagnostic information
            current_index = session_data.get("current_question_index", 0)
            questions_count = len(session_data.get("questions", []))
            responses_count = len(session_data.get("responses", []))
            
            return {
                "status": "found",
                "session_status": session_data["status"],
                "progress": {
                    "questions_answered": responses_count,
                    "current_question": current_index + 1,
                    "total_questions": self.config.MAX_INTERVIEW_QUESTIONS,
                    "questions_available": questions_count
                },
                "start_time": session_data["start_time"],
                "config": session_data["config"],
                "debug_info": {
                    "current_question_index": current_index,
                    "questions_in_cache": questions_count,
                    "responses_submitted": responses_count,
                    "index_valid": current_index < questions_count
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting session status: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _validate_and_repair_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and repair session data to prevent index errors"""
        try:
            # Ensure required fields exist
            if "questions" not in session_data:
                session_data["questions"] = []
            if "responses" not in session_data:
                session_data["responses"] = []
            if "current_question_index" not in session_data:
                session_data["current_question_index"] = 0
            
            # Ensure current_question_index is valid
            current_index = session_data["current_question_index"]
            questions_count = len(session_data["questions"])
            
            # If index is out of bounds, adjust it
            if current_index >= questions_count and questions_count > 0:
                session_data["current_question_index"] = questions_count - 1
                logger.warning(f"⚠️ Adjusted question index from {current_index} to {session_data['current_question_index']}")
            
            # If no questions exist but we need one, generate it
            if questions_count == 0 and current_index == 0:
                logger.warning("⚠️ No questions found in session, generating first question")
                first_question = self._generate_interview_question(session_data, 1)
                if first_question:
                    session_data["questions"].append(first_question)
            
            return session_data
            
        except Exception as e:
            logger.error(f"❌ Error validating session data: {e}")
            return session_data
    
    def _generate_interview_question(self, session_data: Dict[str, Any], 
                                   question_number: int) -> str:
        """Generate contextual interview question"""
        try:
            config = session_data["config"]
            previous_responses = session_data.get("responses", [])
            
            # Build context for question generation
            context_prompt = f"""
            Generate interview question #{question_number} for:
            - Role: {config['role']}
            - Experience: {config['experience']}
            - Industry: {config['industry']}
            
            Previous questions asked: {[q for q in session_data.get('questions', [])]}
            
            Generate a relevant, professional question that:
            1. Matches the role and experience level
            2. Is different from previous questions
            3. Progressively increases in complexity
            4. Is appropriate for the industry
            
            Return only the question text, no additional formatting.
            """
            
            system_message = PromptTemplates.get_interview_system_prompt(
                config['role'], config['experience'], config['industry']
            )
            
            question = self.client.generate_response(context_prompt, system_message)
            return self.formatter.format_response(question)
            
        except Exception as e:
            logger.error(f"❌ Error generating interview question: {e}")
            # Fallback generic question
            return f"Can you tell me about your experience with {session_data['config']['role']} responsibilities?"
    
    def _generate_interview_summary(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive interview summary"""
        try:
            responses = session_data["responses"]
            config = session_data["config"]
            
            # Calculate overall scores
            scores = [r["feedback"].get("score", 0) for r in responses if r["feedback"].get("score")]
            average_score = sum(scores) / len(scores) if scores else 0
            
            # Generate overall assessment
            summary_prompt = f"""
            Provide a comprehensive interview summary for a {config['role']} position.
            
            Interview Details:
            - Role: {config['role']}
            - Experience Level: {config['experience']}
            - Industry: {config['industry']}
            - Questions Answered: {len(responses)}
            - Average Score: {average_score:.1f}/10
            
            Responses Summary:
            {self._format_responses_for_summary(responses)}
            
            Provide:
            1. Overall performance assessment
            2. Key strengths demonstrated
            3. Areas needing improvement
            4. Specific recommendations for career development
            5. Final recommendation (hire/no hire/further review)
            """
            
            system_message = """
            You are an expert interview assessor. Provide a professional, 
            comprehensive evaluation with specific, actionable feedback.
            """
            
            summary_text = self.client.generate_response(summary_prompt, system_message)
            
            return {
                "overall_score": round(average_score, 1),
                "total_questions": len(responses),
                "session_duration": self._calculate_session_duration(session_data),
                "summary": self.formatter.format_response(summary_text),
                "individual_scores": scores,
                "timestamp": timezone.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating interview summary: {e}")
            return {
                "overall_score": 0,
                "summary": "Unable to generate summary",
                "error": str(e)
            }
    
    def _format_responses_for_summary(self, responses: List[Dict[str, Any]]) -> str:
        """Format responses for summary generation"""
        formatted = []
        for i, response in enumerate(responses, 1):
            feedback = response.get("feedback", {})
            score = feedback.get("score", "N/A")
            formatted.append(f"Q{i}: Score {score}/10 - {response.get('answer', '')[:100]}...")
        
        return "\n".join(formatted)
    
    def _calculate_session_duration(self, session_data: Dict[str, Any]) -> str:
        """Calculate interview session duration"""
        try:
            start_time = datetime.fromisoformat(session_data["start_time"].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(session_data.get("end_time", timezone.now().isoformat()).replace('Z', '+00:00'))
            duration = end_time - start_time
            
            minutes = int(duration.total_seconds() // 60)
            seconds = int(duration.total_seconds() % 60)
            
            return f"{minutes}m {seconds}s"
            
        except Exception:
            return "Unknown"


class AnalysisService(BaseService):
    """Professional analysis service for various data analysis tasks"""
    
    def analyze_sentiment(self, text: str, user_id: str = None) -> Dict[str, Any]:
        """Analyze sentiment of provided text"""
        try:
            if not self.validator.validate_prompt(text):
                return {
                    "status": "error",
                    "message": "Invalid text format"
                }
            
            # Check cache
            cache_key = self._get_cache_key("sentiment", text)
            cached_result = self._get_cached_response(cache_key)
            
            if cached_result:
                return cached_result
            
            # Perform analysis
            clean_text = self.validator.sanitize_input(text)
            result = self.client.generate_analysis(clean_text, "sentiment")
            
            # Add metadata
            result["input_length"] = len(clean_text)
            result["user_id"] = user_id
            result["analysis_type"] = "sentiment"
            
            # Cache result
            self._cache_response(cache_key, result)
            
            logger.info(f"✅ Sentiment analysis completed for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in sentiment analysis: {e}")
            return self.error_handler.handle_analysis_error(e)
    
    def analyze_interview_performance(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall interview performance"""
        try:
            # Extract performance data
            responses = session_data.get("responses", [])
            if not responses:
                return {
                    "status": "error",
                    "message": "No interview responses to analyze"
                }
            
            # Prepare analysis data
            analysis_text = self._prepare_interview_data_for_analysis(responses)
            
            # Perform analysis
            result = self.client.generate_analysis(analysis_text, "interview")
            
            # Add interview-specific metrics
            result["session_metrics"] = self._calculate_interview_metrics(responses)
            result["analysis_type"] = "interview_performance"
            
            logger.info("✅ Interview performance analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in interview performance analysis: {e}")
            return self.error_handler.handle_analysis_error(e)
    
    def analyze_user_engagement(self, engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user engagement patterns"""
        try:
            # Prepare engagement data for analysis
            analysis_text = self._prepare_engagement_data_for_analysis(engagement_data)
            
            # Perform analysis
            result = self.client.generate_analysis(analysis_text, "performance")
            
            # Add engagement-specific insights
            result["engagement_metrics"] = self._calculate_engagement_metrics(engagement_data)
            result["analysis_type"] = "user_engagement"
            
            logger.info("✅ User engagement analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in engagement analysis: {e}")
            return self.error_handler.handle_analysis_error(e)
    
    def _prepare_interview_data_for_analysis(self, responses: List[Dict[str, Any]]) -> str:
        """Prepare interview responses for analysis"""
        analysis_data = []
        
        for i, response in enumerate(responses, 1):
            feedback = response.get("feedback", {})
            score = feedback.get("score", 0)
            answer_length = len(response.get("answer", ""))
            
            analysis_data.append(f"""
            Question {i}:
            - Score: {score}/10
            - Answer Length: {answer_length} characters
            - Feedback: {feedback.get('feedback', 'No feedback')}
            """)
        
        return "\n".join(analysis_data)
    
    def _prepare_engagement_data_for_analysis(self, engagement_data: Dict[str, Any]) -> str:
        """Prepare engagement data for analysis"""
        return f"""
        User Engagement Analysis Data:
        - Session Duration: {engagement_data.get('session_duration', 'Unknown')}
        - Pages Visited: {engagement_data.get('pages_visited', 0)}
        - Actions Performed: {engagement_data.get('actions_performed', 0)}
        - Feature Usage: {engagement_data.get('feature_usage', {})}
        - Time Spent: {engagement_data.get('time_spent', {})}
        - User Type: {engagement_data.get('user_type', 'Unknown')}
        """
    
    def _calculate_interview_metrics(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate interview-specific metrics"""
        if not responses:
            return {}
        
        scores = [r["feedback"].get("score", 0) for r in responses if r["feedback"].get("score")]
        answer_lengths = [len(r.get("answer", "")) for r in responses]
        
        return {
            "average_score": sum(scores) / len(scores) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "total_questions": len(responses),
            "average_answer_length": sum(answer_lengths) / len(answer_lengths) if answer_lengths else 0,
            "score_trend": self._calculate_score_trend(scores)
        }
    
    def _calculate_engagement_metrics(self, engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate engagement-specific metrics"""
        return {
            "engagement_score": self._calculate_engagement_score(engagement_data),
            "activity_level": self._determine_activity_level(engagement_data),
            "feature_adoption": self._calculate_feature_adoption(engagement_data)
        }
    
    def _calculate_score_trend(self, scores: List[float]) -> str:
        """Calculate if scores are improving, declining, or stable"""
        if len(scores) < 2:
            return "insufficient_data"
        
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 0.5:
            return "improving"
        elif second_avg < first_avg - 0.5:
            return "declining"
        else:
            return "stable"
    
    def _calculate_engagement_score(self, data: Dict[str, Any]) -> float:
        """Calculate overall engagement score"""
        # Simple engagement scoring algorithm
        score = 0.0
        
        # Session duration factor
        duration = data.get('session_duration', 0)
        if duration > 1800:  # 30 minutes
            score += 3.0
        elif duration > 900:  # 15 minutes
            score += 2.0
        elif duration > 300:  # 5 minutes
            score += 1.0
        
        # Activity factor
        actions = data.get('actions_performed', 0)
        score += min(actions * 0.1, 3.0)
        
        # Feature usage factor
        features_used = len(data.get('feature_usage', {}))
        score += min(features_used * 0.5, 4.0)
        
        return min(score, 10.0)  # Cap at 10
    
    def _determine_activity_level(self, data: Dict[str, Any]) -> str:
        """Determine user activity level"""
        score = self._calculate_engagement_score(data)
        
        if score >= 7.0:
            return "high"
        elif score >= 4.0:
            return "medium"
        else:
            return "low"
    
    def _calculate_feature_adoption(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate feature adoption rates"""
        feature_usage = data.get('feature_usage', {})
        total_sessions = data.get('total_sessions', 1)
        
        adoption_rates = {}
        for feature, usage_count in feature_usage.items():
            adoption_rates[feature] = min(usage_count / total_sessions, 1.0)
        
        return adoption_rates
