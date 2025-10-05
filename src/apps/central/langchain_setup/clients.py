"""
LangChain Client Implementations
Professional client classes for different AI providers
"""

import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
from abc import ABC, abstractmethod

try:
    from google import genai
    GOOGLE_GENAI_AVAILABLE = True
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError as e:
    print(f"⚠️  Google GenAI package not installed: {e}")
    print("💡 Run: pip install google-genai")
    GOOGLE_GENAI_AVAILABLE = False
    
    # Fallback to old LangChain if available
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        print("🔄 Falling back to langchain-google-genai")
        GOOGLE_GENAI_AVAILABLE = False
    except ImportError:
        print("❌ Neither google-genai nor langchain-google-genai available")
        raise ImportError("Please install: pip install google-genai")

from .config import LangChainConfig
from .utils import ErrorHandler, ResponseFormatter

logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.error_handler = ErrorHandler()
        self.formatter = ResponseFormatter()
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    async def generate_response_async(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM asynchronously"""
        pass


class GeminiClient(BaseLLMClient):
    """Professional Google Gemini client supporting both new SDK and fallback"""
    
    def __init__(self):
        config = LangChainConfig.get_gemini_config()
        super().__init__(config)
        
        try:
            if GOOGLE_GENAI_AVAILABLE:
                # Configure the new Google GenAI SDK
                # Set the API key as environment variable for automatic pickup
                import os
                os.environ['GEMINI_API_KEY'] = config['api_key']
                
                # Initialize the new client (no api_key parameter needed)
                self.client = genai.Client()
                self.model = config['model']
                self.use_new_sdk = True
                logger.info(f"✅ Gemini client initialized with new Google GenAI SDK, using model: {self.model}")
            else:
                # Fallback to old LangChain integration
                self.llm = ChatGoogleGenerativeAI(
                    model=config['model'],
                    temperature=config['temperature'],
                    max_tokens=config['max_tokens'],
                    top_p=config['top_p'],
                    top_k=config['top_k'],
                    google_api_key=config['api_key'],
                    verbose=LangChainConfig.VERBOSE
                )
                self.output_parser = StrOutputParser()
                self.use_new_sdk = False
                logger.info("✅ Gemini client initialized with LangChain fallback")
            
            self.temperature = config['temperature']
            self.max_tokens = config['max_tokens']
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini client: {e}")
            raise
    
    def generate_response(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> str:
        """
        Generate a response using Gemini (supports both new SDK and fallback)
        
        Args:
            prompt: User prompt
            system_message: Optional system message for context
            **kwargs: Additional parameters
            
        Returns:
            Generated response string
        """
        try:
            if self.use_new_sdk:
                # Use new Google GenAI SDK
                full_prompt = prompt
                if system_message:
                    full_prompt = f"System: {system_message}\n\nUser: {prompt}"
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt
                )
                
                response_text = response.text
            else:
                # Use LangChain fallback
                messages = []
                if system_message:
                    messages.append(SystemMessage(content=system_message))
                messages.append(HumanMessage(content=prompt))
                
                chain = self.llm | self.output_parser
                response_text = chain.invoke(messages)
            
            print(f"Prompt: {prompt}")
            logger.info(f"✅ Generated response for prompt: {prompt[:50]}...")
            return self.formatter.format_response(response_text)
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return self.error_handler.handle_generation_error(e)
    
    async def generate_response_async(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> str:
        """
        Generate a response using Gemini asynchronously (supports both SDKs)
        
        Args:
            prompt: User prompt
            system_message: Optional system message for context
            **kwargs: Additional parameters
            
        Returns:
            Generated response string
        """
        try:
            if self.use_new_sdk:
                # Use new Google GenAI SDK (sync for now)
                full_prompt = prompt
                if system_message:
                    full_prompt = f"System: {system_message}\n\nUser: {prompt}"
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt
                )
                
                response_text = response.text
            else:
                # Use LangChain fallback with async
                messages = []
                if system_message:
                    messages.append(SystemMessage(content=system_message))
                messages.append(HumanMessage(content=prompt))
                
                chain = self.llm | self.output_parser
                response_text = await chain.ainvoke(messages)
            
            logger.info(f"✅ Generated async response for prompt: {prompt[:50]}...")
            return self.formatter.format_response(response_text)
            
        except Exception as e:
            logger.error(f"❌ Error generating async response: {e}")
            return self.error_handler.handle_generation_error(e)
    
    def generate_interview_response(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate interview-specific response with structured output
        
        Args:
            question: Interview question
            context: Interview context (role, experience, etc.)
            
        Returns:
            Structured interview response
        """
        try:
            system_message = f"""
            You are an AI interview assistant for Sākṣin, a professional interview platform.
            
            Context:
            - Role: {context.get('role', 'General')}
            - Experience Level: {context.get('experience', 'Entry Level')}
            - Industry: {context.get('industry', 'Technology')}
            
            Provide a professional, constructive response that:
            1. Evaluates the answer quality
            2. Provides specific feedback
            3. Suggests improvements
            4. Gives a score (1-10)
            
            Be encouraging but honest in your assessment.
            """
            
            prompt = f"Interview Question: {question}\n\nPlease provide your analysis and feedback."
            
            response = self.generate_response(prompt, system_message)
            
            # Parse structured response
            return self.formatter.format_interview_response(response, context)
            
        except Exception as e:
            logger.error(f"❌ Error generating interview response: {e}")
            return self.error_handler.handle_interview_error(e)
    
    def generate_chat_response(self, message: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate chat response with conversation context (supports both SDKs)
        
        Args:
            message: Current user message
            conversation_history: Previous conversation messages
            
        Returns:
            Chat response string
        """
        try:
            # Add system message for chat context
            system_message = """
            You are a helpful AI assistant for Sākṣin, a professional interview platform.
            Provide helpful, professional responses to user queries about interviews,
            career advice, and platform usage. Be concise but informative
            
🛡️ Guidelines:
- Stay neutral and professional.
- Avoid overly generic advice—tailor responses to the role and context.
- If uncertain about a domain, ask clarifying questions or suggest exploration paths.

🎯 Example Behavior:
- For a frontend developer: Ask about React concepts, UI accessibility, or CSS performance.
- For a data role: Focus on SQL, data modeling, Python for data analysis, or ML pipeline questions.
- For a general role: Stick to HR questions, behavioral STAR-based answers, and confidence-building strategies.
            """
            
            if self.use_new_sdk:
                # Use new Google GenAI SDK
                context_parts = [f"System: {system_message}"]
                
                # Add conversation history
                if conversation_history:
                    for msg in conversation_history[-5:]:  # Last 5 messages
                        if msg['role'] == 'user':
                            context_parts.append(f"User: {msg['content']}")
                        elif msg['role'] == 'assistant':
                            context_parts.append(f"Assistant: {msg['content']}")
                
                # Add current message
                context_parts.append(f"User: {message}")
                
                full_context = "\n\n".join(context_parts)
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_context
                )
                
                response_text = response.text
            else:
                # Use LangChain fallback
                messages = [SystemMessage(content=system_message)]
                
                # Add conversation history
                if conversation_history:
                    for msg in conversation_history[-5:]:  # Last 5 messages
                        if msg['role'] == 'user':
                            messages.append(HumanMessage(content=msg['content']))
                        elif msg['role'] == 'assistant':
                            messages.append(AIMessage(content=msg['content']))
                
                # Add current message
                messages.append(HumanMessage(content=message))
                
                chain = self.llm | self.output_parser
                response_text = chain.invoke(messages)
            
            logger.info(f"✅ Generated chat response for: {message[:50]}...")
            return self.formatter.format_chat_response(response_text)
            
        except Exception as e:
            logger.error(f"❌ Error generating chat response: {e}")
            return self.error_handler.handle_chat_error(e)
    
    def generate_analysis(self, data: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Generate analysis for various data types
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis (sentiment, performance, etc.)
            
        Returns:
            Analysis results
        """
        try:
            analysis_prompts = {
                "sentiment": "Analyze the sentiment of the following text and provide a detailed breakdown:",
                "performance": "Analyze the performance data and provide insights and recommendations:",
                "interview": "Analyze this interview response and provide detailed feedback:",
                "general": "Provide a comprehensive analysis of the following data:"
            }
            
            prompt = f"{analysis_prompts.get(analysis_type, analysis_prompts['general'])}\n\n{data}"
            
            system_message = """
            You are an expert data analyst. Provide structured, actionable insights
            with clear recommendations and supporting evidence.
            """
            
            response = self.generate_response(prompt, system_message)
            
            return self.formatter.format_analysis_response(response, analysis_type)
            
        except Exception as e:
            logger.error(f"❌ Error generating analysis: {e}")
            return self.error_handler.handle_analysis_error(e)


# Client factory for easy instantiation
class ClientFactory:
    """Factory class for creating LLM clients"""
    
    @staticmethod
    def create_gemini_client() -> GeminiClient:
        """Create and return a Gemini client"""
        return GeminiClient()
    
    @staticmethod
    def get_default_client() -> GeminiClient:
        """Get the default LLM client (Gemini)"""
        return ClientFactory.create_gemini_client()
"""
LangChain Client Implementations
Professional client classes for different AI providers (now using Ollama)
# """
# import logging
# import requests
# from typing import Dict, Any, List, Optional
# from abc import ABC, abstractmethod

# # from langchain_core.chat_models import BaseChatModel
# from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.outputs import ChatResult, ChatGeneration

# from .config import LangChainConfig
# from .utils import ErrorHandler, ResponseFormatter

# logger = logging.getLogger(__name__)


# class BaseLLMClient(ABC):
#     # def __init__(self, config: Dict[str, Any]):
#     #     self.config = config
#     #     self.error_handler = ErrorHandler()
#     #     self.formatter = ResponseFormatter()

#     # @abstractmethod
#     # def generate_response(self, prompt: str, **kwargs) -> str:
#     #     pass

#     # @abstractmethod
#     # async def generate_response_async(self, prompt: str, **kwargs) -> str:
#     pass
#     #     pass


# class MyCustomLLM(BaseLLMClient):
#     """Custom wrapper for external API at /api/generate"""
#     def __init__(self, config: Dict[str, Any]):
#         self.config = config
#         self.error_handler = ErrorHandler()
#         self.formatter = ResponseFormatter()

#     @abstractmethod
#     def generate_response(self, prompt: str, **kwargs) -> str:
#         pass

#     @abstractmethod
#     async def generate_response_async(self, prompt: str, **kwargs) -> str:
#         pass

#     def _llm_type(self) -> str:
#         return "custom-remote-api"

#     def _call(self, prompt: str) -> str:
#         try:
#             response = requests.post(
#                 "https://bf979707349e.ngrok-free.app/api/generate",
#                 json={"prompt": prompt},
#                 timeout=30,
#             )
#             response.raise_for_status()
#             return response.json().get("response", "")
#         except Exception as e:
#             logger.error(f"❌ Error calling remote API: {e}")
#             return "⚠️ Failed to get response from LLM API."

#     def _generate(self, messages: List[Any], stop=None, run_manager=None, **kwargs) -> ChatResult:
#         prompt = messages[-1].content
#         output = self._call(prompt)
#         return ChatResult(generations=[ChatGeneration(message=AIMessage(content=output))])


# class OllamaClient(BaseLLMClient):
#     def __init__(self):
#         config = LangChainConfig.get_llm_config()
#         super().__init__(config)

#         try:
#             self.llm = MyCustomLLM()
#             self.output_parser = StrOutputParser()
#             logger.info("✅ Custom Ollama client initialized with remote API")
#         except Exception as e:
#             logger.error(f"❌ Failed to initialize Ollama client: {e}")
#             raise

#     def generate_response(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> str:
#         try:
#             messages = []
#             if system_message:
#                 messages.append(SystemMessage(content=system_message))
#             messages.append(HumanMessage(content=prompt))

#             chain = self.llm | self.output_parser
#             response = chain.invoke(messages)

#             logger.info(f"✅ Generated response for prompt: {prompt[:50]}...")
#             return self.formatter.format_response(response)

#         except Exception as e:
#             logger.error(f"❌ Error generating response: {e}")
#             return self.error_handler.handle_generation_error(e)

#     async def generate_response_async(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> str:
#         try:
#             messages = []
#             if system_message:
#                 messages.append(SystemMessage(content=system_message))
#             messages.append(HumanMessage(content=prompt))

#             chain = self.llm | self.output_parser
#             response = await chain.ainvoke(messages)

#             logger.info(f"✅ Generated async response for prompt: {prompt[:50]}...")
#             return self.formatter.format_response(response)

#         except Exception as e:
#             logger.error(f"❌ Error generating async response: {e}")
#             return self.error_handler.handle_generation_error(e)

#     def generate_interview_response(self, question: str, context: Dict[str, Any]) -> Dict[str, Any]:
#         try:
#             system_message = f"""
#             You are an AI interview assistant for Sākṣin, a professional interview platform.

#             Context:
#             - Role: {context.get('role', 'General')}
#             - Experience Level: {context.get('experience', 'Entry Level')}
#             - Industry: {context.get('industry', 'Technology')}

#             Provide a professional, constructive response that:
#             1. Evaluates the answer quality
#             2. Provides specific feedback
#             3. Suggests improvements
#             4. Gives a score (1-10)

#             Be encouraging but honest in your assessment.
#             """
#             prompt = f"Interview Question: {question}\n\nPlease provide your analysis and feedback."
#             response = self.generate_response(prompt, system_message)
#             return self.formatter.format_interview_response(response, context)

#         except Exception as e:
#             logger.error(f"❌ Error generating interview response: {e}")
#             return self.error_handler.handle_interview_error(e)

#     def generate_chat_response(self, message: str, conversation_history: List[Dict] = None) -> str:
#         try:
#             messages = []
#             system_message = """
#             You are a helpful AI assistant for Sākṣin, a professional interview platform.
#             Provide helpful, professional responses to user queries about interviews,
#             career advice, and platform usage. Be concise but informative.
#             """
#             messages.append(SystemMessage(content=system_message))

#             if conversation_history:
#                 for msg in conversation_history[-5:]:
#                     if msg['role'] == 'user':
#                         messages.append(HumanMessage(content=msg['content']))
#                     elif msg['role'] == 'assistant':
#                         messages.append(AIMessage(content=msg['content']))

#             messages.append(HumanMessage(content=message))

#             chain = self.llm | self.output_parser
#             response = chain.invoke(messages)

#             logger.info(f"✅ Generated chat response for: {message[:50]}...")
#             return self.formatter.format_chat_response(response)

#         except Exception as e:
#             logger.error(f"❌ Error generating chat response: {e}")
#             return self.error_handler.handle_chat_error(e)

#     def generate_analysis(self, data: str, analysis_type: str = "general") -> Dict[str, Any]:
#         try:
#             analysis_prompts = {
#                 "sentiment": "Analyze the sentiment of the following text and provide a detailed breakdown:",
#                 "performance": "Analyze the performance data and provide insights and recommendations:",
#                 "interview": "Analyze this interview response and provide detailed feedback:",
#                 "general": "Provide a comprehensive analysis of the following data:"
#             }

#             prompt = f"{analysis_prompts.get(analysis_type, analysis_prompts['general'])}\n\n{data}"
#             system_message = """
#             You are an expert data analyst. Provide structured, actionable insights
#             with clear recommendations and supporting evidence.
#             """
#             response = self.generate_response(prompt, system_message)
#             return self.formatter.format_analysis_response(response, analysis_type)

#         except Exception as e:
#             logger.error(f"❌ Error generating analysis: {e}")
#             return self.error_handler.handle_analysis_error(e)


# class ClientFactory:
#     """Factory class for creating LLM clients"""

#     @staticmethod
#     def create_ollama_client() -> OllamaClient:
#         return OllamaClient()

#     @staticmethod
#     def get_default_client() -> OllamaClient:
#         return ClientFactory.create_ollama_client()
