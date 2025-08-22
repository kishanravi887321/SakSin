# 🎓 **Sākṣin** — AI-Powered MOOC Interview Platform

[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-blue.svg)](https://www.django-rest-framework.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-purple.svg)](https://python.langchain.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io/)

**Sākṣin** is a cutting-edge AI-driven interview platform that revolutionizes MOOC (Massive Open Online Course) assessment through intelligent real-time evaluation. The platform leverages advanced Large Language Models, facial emotion analysis, and sophisticated memory management to deliver human-like interview experiences that prepare learners for real-world technical challenges.

---

## 🌟 **Key Features**

### 🤖 **Advanced AI Interview Engine**
- **Dynamic Question Generation**: Context-aware questioning using Google Gemini and LangChain
- **Intelligent Follow-ups**: AI-powered conversation flow that adapts to candidate responses
- **Multi-Domain Support**: Technical, behavioral, and industry-specific interview scenarios
- **Real-time Response Analysis**: Instant evaluation of answers with detailed feedback

### 🧠 **Sophisticated Memory Management**
- **Redis-Powered Sessions**: Persistent conversation history across disconnections
- **Smart Summarization**: Token-efficient long conversation handling
- **Context Preservation**: Maintains interview flow and candidate progress
- **Multi-Session Support**: Parallel interview management for multiple users

### 📊 **Comprehensive Analytics**
- **Real-time Performance Metrics**: Live scoring and assessment tracking
- **Detailed Evaluation Reports**: AI-generated feedback with strengths/weaknesses
- **Category-wise Analysis**: Technical, communication, and confidence scoring
- **Progress Tracking**: Historical performance and improvement suggestions

### 🔐 **Enterprise-Grade Security**
- **JWT Authentication**: Secure token-based user management
- **Role-Based Access Control**: Admin, instructor, and student permissions
- **Data Encryption**: Secure storage of interview data and user information
- **CORS Configuration**: Safe cross-origin resource sharing

### 📸 **Advanced Emotion Detection** *(Under Development)*
- **WebRTC Integration**: Real-time video capture during interviews *(In Progress)*
- **DeepFace Analysis**: Facial expression and confidence assessment *(Under Development)*
- **Behavioral Insights**: Non-verbal communication evaluation *(Planned)*
- **Real-time Emotion Tracking**: Live facial emotion monitoring during interviews *(In Development)*
- **Confidence Level Assessment**: AI-powered body language analysis *(Coming Soon)*

---

## 🏗️ **System Architecture & Workflow**

```mermaid
flowchart TD
    %% User Journey Start
    USER[User] --> LOGIN{Login/Register}
    LOGIN -->|New User| REGISTER[Registration]
    LOGIN -->|Existing User| AUTH[Authentication]
    
    REGISTER --> PROFILE[Create Profile]
    AUTH --> DASHBOARD[Dashboard]
    PROFILE --> DASHBOARD
    
    %% Main Application Flow
    DASHBOARD --> CHOICE{Choose Action}
    CHOICE -->|Start Interview| INTERVIEW_CONFIG[Interview Configuration]
    CHOICE -->|Chat with AI| CHAT_START[Chat Interface]
    CHOICE -->|View Analytics| ANALYTICS_VIEW[Performance Analytics]
    CHOICE -->|Manage Subscription| SUBSCRIPTION[Subscription Management]
    
    %% Interview Workflow
    INTERVIEW_CONFIG --> INTERVIEW_START[Start Interview Session]
    INTERVIEW_START --> QUESTION_GENERATION[AI Question Generation]
    QUESTION_GENERATION --> USER_ANSWER[User Answers]
    USER_ANSWER --> RESPONSE_ANALYSIS[AI Response Analysis]
    RESPONSE_ANALYSIS --> NEXT_QUESTION{More Questions?}
    NEXT_QUESTION -->|Yes| QUESTION_GENERATION
    NEXT_QUESTION -->|No| INTERVIEW_EVALUATION[Final Evaluation]
    
    %% Chat Workflow
    CHAT_START --> CHAT_MESSAGE[Send Message]
    CHAT_MESSAGE --> AI_PROCESSING[AI Processing]
    AI_PROCESSING --> AI_RESPONSE[AI Response]
    AI_RESPONSE --> CHAT_CONTINUE{Continue Chat?}
    CHAT_CONTINUE -->|Yes| CHAT_MESSAGE
    CHAT_CONTINUE -->|No| CHAT_END[End Chat]
    
    %% Backend Processing Layer
    QUESTION_GENERATION --> LANGCHAIN[LangChain]
    RESPONSE_ANALYSIS --> LANGCHAIN
    AI_PROCESSING --> LANGCHAIN
    
    LANGCHAIN <--> GEMINI[Google Gemini AI]
    LANGCHAIN <--> PROMPT_TEMPLATES[Prompt Templates]
    LANGCHAIN <--> CONTEXT_MEMORY[Context Memory]
    
    %% Data Storage & Caching
    USER_ANSWER --> REDIS_CACHE[Redis Cache]
    AI_RESPONSE --> REDIS_CACHE
    INTERVIEW_EVALUATION --> POSTGRES_DB[PostgreSQL]
    CHAT_END --> POSTGRES_DB
    
    %% External Services Integration
    INTERVIEW_EVALUATION --> EMAIL_SERVICE[Email Report]
    SUBSCRIPTION --> PAYMENT_GATEWAY[Razorpay]
    PROFILE --> FILE_STORAGE[Cloudinary]
    
    %% Results & Feedback
    INTERVIEW_EVALUATION --> REPORT_GENERATION[Generate Report]
    REPORT_GENERATION --> FEEDBACK_DELIVERY[Deliver Feedback]
    FEEDBACK_DELIVERY --> DASHBOARD
    
    EMAIL_SERVICE --> USER
    ANALYTICS_VIEW --> DASHBOARD
    
    %% Clean styling with white text for dark theme compatibility
    classDef userFlow stroke:#1976d2,stroke-width:3px,color:#fff,fill:transparent
    classDef aiProcess stroke:#f57c00,stroke-width:3px,color:#fff,fill:transparent
    classDef dataStore stroke:#7b1fa2,stroke-width:3px,color:#fff,fill:transparent
    classDef external stroke:#388e3c,stroke-width:3px,color:#fff,fill:transparent
    classDef decision stroke:#d32f2f,stroke-width:3px,color:#fff,fill:transparent
    
    class USER,LOGIN,REGISTER,PROFILE,DASHBOARD userFlow
    class QUESTION_GENERATION,RESPONSE_ANALYSIS,AI_PROCESSING,LANGCHAIN,GEMINI aiProcess
    class REDIS_CACHE,POSTGRES_DB,CONTEXT_MEMORY dataStore
    class EMAIL_SERVICE,PAYMENT_GATEWAY,FILE_STORAGE external
    class CHOICE,NEXT_QUESTION,CHAT_CONTINUE decision
```

### **📋 Platform Workflow Overview**

#### **🎯 User Journey Flow**
1. **🔐 Authentication**: User registration/login with JWT tokens
2. **👤 Profile Setup**: User creates profile with role and experience
3. **📊 Dashboard**: Central hub for accessing all platform features
4. **🎯 Action Selection**: Choose between Interview, Chat, Analytics, or Subscription

#### **🎯 Interview Workflow**
1. **⚙️ Configuration**: Set role, experience level, and interview type
2. **🎬 Session Start**: Initialize AI-powered interview session
3. **🤖 Question Generation**: LangChain + Gemini generate contextual questions
4. **🎤 User Response**: Candidate provides answers (text/voice)
5. **🔍 Analysis**: AI evaluates response quality and generates follow-ups
6. **🔄 Iteration**: Continue until interview completion
7. **📊 Evaluation**: Generate comprehensive performance report

#### **💬 Chat Workflow**
1. **💬 Message Input**: User sends message to AI assistant
2. **🧠 AI Processing**: LangChain processes with context memory
3. **🤖 Response Generation**: Gemini generates helpful response
4. **🔄 Conversation**: Maintains context across multiple exchanges

#### **🗄️ Data Management**
- **⚡ Redis**: Real-time session management and response caching
- **🗄️ PostgreSQL**: Persistent storage for users, interviews, and analytics
- **🧠 Context Memory**: Maintains conversation history and interview state
- **📝 Prompt Templates**: Structured prompts for consistent AI behavior

#### **🌐 External Integrations**
- **📧 Email Service**: Automated report delivery and notifications
- **💳 Payment Gateway**: Subscription management and billing
- **☁️ File Storage**: Profile images and document management
- **📚 API Documentation**: Swagger-based developer documentation

---

## 📁 **Project Structure**

```
SakSIn/
├── 📂 config/                      # Django configuration
│   ├── settings.py                 # Main settings & environment config
│   ├── urls.py                     # Root URL routing
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── 📂 apps/                        # Application modules
│   ├── 📂 accounts/                # User management & authentication
│   │   ├── models.py               # Custom User model with roles
│   │   ├── serializers.py          # JWT & user data serializers
│   │   ├── views.py                # Auth endpoints & user management
│   │   └── api/                    # API routes for accounts
│   │
│   ├── 📂 central/                 # Core AI interview system
│   │   ├── 📂 langchain_setup/     # LangChain integration layer
│   │   │   ├── clients.py          # AI client implementations
│   │   │   ├── services.py         # High-level service classes
│   │   │   ├── config.py           # LangChain configuration
│   │   │   └── utils.py            # Utilities & helpers
│   │   ├── views.py                # Interview API endpoints
│   │   ├── serializers.py          # Request/response serializers
│   │   └── models.py               # Interview session models
│   │
│   ├── 📂 interviews/              # Interview management
│   ├── 📂 analytics/               # Performance analytics
│   ├── 📂 subscriptions/           # Payment & subscription logic
│   └── 📂 auth/                    # Extended authentication
│
├── 📂 static/                      # Static files
├── 📂 media/                       # User uploads
├── requirements.txt                # Python dependencies
├── manage.py                       # Django management script
└── README.md                       # Project documentation
```

---

## 🚀 **Quick Start Guide**

### **Prerequisites**
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Google Gemini API Key

### **1. Environment Setup**

```powershell
# Clone the repository
git clone <repository-url>
cd SakSIn

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Environment Configuration**

Create `.env` file in the root directory:

```env
# Database Configuration
DB_URL=postgresql://username:password@localhost:5432/saksin_db

# Security
SECRET_KEY=your-super-secret-django-key
DEBUG=True

# AI Configuration
GOOGLE_GEMINI_API_KEY=your-gemini-api-key

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Service (Brevo)
BREVO_API_KEY_EMAIL=your-brevo-api-key
FORWARDING_EMAIL=your-email@domain.com

# Cloud Storage (Cloudinary)
CLOUD_NAME=your-cloudinary-name
API_KEY=your-cloudinary-key
API_SECRET=your-cloudinary-secret

# Payment Gateway (Razorpay)
RAZORPAY_API_ID=your-razorpay-id
RAZORPAY_API_SECRET=your-razorpay-secret
PAYMENT_AMOUNT_RS=100

# JWT Configuration
ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=1
```

### **3. Database Setup**

```powershell
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### **4. Launch Application**

```powershell
# Start development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

---

## 📚 **API Documentation**

### **Authentication Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | User registration |
| POST | `/api/users/login/` | User authentication |
| POST | `/api/users/token/refresh/` | Refresh JWT token |
| POST | `/api/users/update-password/` | Update password |
| POST | `/api/users/forget-password/` | Forgot password |
| GET | `/api/users/profile/` | Get user profile |
| PUT | `/api/users/profile/update/` | Update user profile |
| POST | `/api/users/auth/google/` | Google OAuth login |

### **AI & Interview System Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/central/v1/interview/start/` | Initialize interview session |
| POST | `/api/central/v1/interview/answer/` | Submit interview response |
| GET | `/api/central/v1/interview/status/` | Check interview progress |
| POST | `/api/central/v1/chat/send/` | Chat with AI assistant |
| GET | `/api/central/v1/chat/history/` | Retrieve chat history |
| POST | `/api/central/v1/analysis/analyze/` | Get performance analysis |
| GET | `/api/central/v1/health/` | Health check endpoint |
| GET | `/api/central/v1/health/test/` | Test endpoint |

### **Documentation & Admin**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/docs/` | Swagger API Documentation |
| GET | `/redoc/` | ReDoc API Documentation |
| GET | `/admin/` | Django Admin Interface |

### **Request/Response Examples**

#### **User Registration**
```json
POST /api/users/register/
{
    "username": "johndoe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123",
    "name": "John Doe"
}
```

#### **Start Interview Session**
```json
POST /api/central/v1/interview/start/
{
    "role": "Full Stack Developer",
    "experience": "3-5 years",
    "industry": "Technology",
    "interview_type": "technical",
    "difficulty": "intermediate"
}
```

#### **Submit Interview Answer**
```json
POST /api/central/v1/interview/answer/
{
    "session_id": "interview_123",
    "answer": "I would use React hooks for state management...",
    "question_id": "q1"
}
```

#### **Chat with AI Assistant**
```json
POST /api/central/v1/chat/send/
{
    "message": "Can you explain the difference between REST and GraphQL?",
    "conversation_id": "chat_456"
}
```

---

## 🔧 **Technology Stack**

### **Backend Framework**
- **Django 5.2.4**: Robust web framework with ORM
- **Django REST Framework**: Professional API development
- **PostgreSQL**: Primary database for structured data
- **Redis**: Caching and session management

### **AI & Machine Learning**
- **LangChain**: AI application framework
- **Google Gemini**: Advanced language model
- **Ollama**: Local LLM support (optional)
- **Custom AI Services**: Interview-specific AI logic

### **Authentication & Security**
- **JWT**: Token-based authentication
- **django-cors-headers**: CORS management
- **Swagger/OpenAPI**: API documentation

### **Cloud Services**
- **Cloudinary**: File storage and CDN
- **Brevo**: Email service provider
- **Razorpay**: Payment processing

### **Development Tools**
- **drf-yasg**: Swagger documentation
- **python-decouple**: Environment management
- **psycopg2**: PostgreSQL adapter

---

## 🧪 **Testing**

### **Run Test Suite**
```powershell
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.accounts
python manage.py test apps.central

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### **API Testing**
The project includes comprehensive test files:
- `test_api_debug.py`: API endpoint testing
- `test_client_fixes.py`: AI client validation
- `test_interview_debug.py`: Interview flow testing
- `test_langchain_setup.py`: LangChain integration tests

---

## 📈 **Performance Features**

### **Caching Strategy**
- **Redis Integration**: Fast session and response caching
- **Database Optimization**: Efficient query patterns
- **Response Compression**: Reduced payload sizes

### **Scalability**
- **Asynchronous Processing**: Non-blocking AI operations
- **Connection Pooling**: Optimized database connections
- **Load Balancing Ready**: Horizontal scaling support

### **Monitoring**
- **Comprehensive Logging**: Detailed application logs
- **Error Tracking**: Professional error handling
- **Performance Metrics**: Response time monitoring

---

## 🔒 **Security Features**

### **Data Protection**
- **Encrypted Storage**: Secure data handling
- **Input Validation**: Comprehensive request validation
- **SQL Injection Prevention**: ORM-based queries

### **Access Control**
- **Role-Based Permissions**: Admin, instructor, student roles
- **JWT Token Management**: Secure authentication flow
- **CORS Configuration**: Safe cross-origin requests

### **Privacy Compliance**
- **Data Anonymization**: Privacy-first approach
- **Audit Trails**: Complete action logging
- **GDPR Ready**: European privacy standards

---

## 🤝 **Contributing**

We welcome contributions to improve Sākṣin! Please follow these guidelines:

### **Development Workflow**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Code Standards**
- Follow PEP 8 Python style guide
- Write comprehensive docstrings
- Include unit tests for new features
- Update API documentation

### **Issue Reporting**
- Use GitHub Issues for bug reports
- Provide detailed reproduction steps
- Include environment information

---

## 🧩 **Architecture Overview**

```text
                +------------------+
                |   Frontend (Next.js)   |
                +----------+-------+
                           |
        +------------------+------------------+
        | WebRTC Video Feed     | WebSockets Chat |
        |                      |                  |
+---------------+     +----------------+     +-----------------+
|  DeepFace API |<--->| Django + DRF   |<--->| LangChain + LLM |
+---------------+     +----------------+     +-----------------+
                           |
                  +--------+--------+
                  |    Redis Memory  |
                  +-----------------+
```



##  **Acknowledgments**

- **LangChain Community**: For the excellent AI framework
- **Google**: For the powerful Gemini API
- **Django Team**: For the robust web framework
- **Redis Labs**: For high-performance caching
- **PostgreSQL**: For reliable data storage

**Built with ❤️ by the Sākṣin Team**

*Transforming education through intelligent assessment ||  IN the progress*
