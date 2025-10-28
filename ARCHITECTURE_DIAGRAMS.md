# 🏗️ Sākṣin Architecture Diagrams

## 1️⃣ DFD Level 2 - User Management (Authentication Process)

```mermaid
flowchart TB
    subgraph "User Management System"
        USER[User] -->|Login Request| AUTH[Authentication Module]
        USER -->|Register Request| REG[Registration Module]
        
        AUTH -->|Validate Credentials| DB[(User Database)]
        REG -->|Store User Data| DB
        
        DB -->|User Data| AUTH
        AUTH -->|JWT Token| USER
        
        AUTH -->|Failed| ERROR[Error Handler]
        ERROR -->|Error Message| USER
        
        REG -->|Success| PROFILE[Profile Creation]
        PROFILE -->|Profile Data| DB
        PROFILE -->|Confirmation| USER
    end
    
    style USER fill:#fff,stroke:#000,stroke-width:3px,color:#000
    style AUTH fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style REG fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style DB fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style ERROR fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style PROFILE fill:#fff,stroke:#000,stroke-width:2px,color:#000
```

---

## 2️⃣ DFD Level 1 - System Overview

```mermaid
flowchart LR
    USER[👤 User] -->|Input| SYSTEM[Sākṣin System]
    SYSTEM -->|Output| USER
    
    SYSTEM <-->|Data| DATABASE[(📊 Database)]
    SYSTEM <-->|AI Requests| GEMINI[🤖 Google Gemini AI]
    SYSTEM <-->|Cache| REDIS[(⚡ Redis Cache)]
    
    ADMIN[👨‍💼 Admin] -->|Manage| SYSTEM
    SYSTEM -->|Reports| ADMIN
    
    style USER fill:#fff,stroke:#000,stroke-width:3px,color:#000
    style SYSTEM fill:#fff,stroke:#000,stroke-width:3px,color:#000
    style DATABASE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style GEMINI fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style REDIS fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style ADMIN fill:#fff,stroke:#000,stroke-width:3px,color:#000
```

---

## 3️⃣ DFD Level 4 - Detailed Process Flow

```mermaid
flowchart TB
    subgraph "Detailed Interview Process"
        START[Start Interview] --> CONFIG[Configure Settings]
        CONFIG -->|Role, Experience| SETUP[Setup Session]
        
        SETUP --> GEN_Q[Generate Question]
        GEN_Q -->|AI Processing| GEMINI[Google Gemini]
        GEMINI -->|Question| DISPLAY[Display Question]
        
        DISPLAY -->|User Answers| CAPTURE[Capture Response]
        CAPTURE -->|Text| ANALYZE[Analyze Response]
        ANALYZE -->|AI Evaluation| GEMINI
        
        GEMINI -->|Feedback| STORE[Store Results]
        STORE --> CACHE[(Redis Cache)]
        STORE --> DB[(PostgreSQL)]
        
        ANALYZE --> DECISION{More Questions?}
        DECISION -->|Yes| GEN_Q
        DECISION -->|No| FINAL[Final Evaluation]
        
        FINAL --> REPORT[Generate Report]
        REPORT --> EMAIL[Send Email]
        REPORT --> DISPLAY_RESULT[Display Results]
        
        DISPLAY_RESULT --> END[End Session]
    end
    
    style START fill:#fff,stroke:#000,stroke-width:3px,color:#000
    style CONFIG fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style SETUP fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style GEN_Q fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style GEMINI fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style DISPLAY fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style CAPTURE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style ANALYZE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style STORE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style CACHE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style DB fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style DECISION fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style FINAL fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style REPORT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style EMAIL fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style DISPLAY_RESULT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style END fill:#fff,stroke:#000,stroke-width:3px,color:#000
```

---

## 4️⃣ DFD Level 0 - Context Diagram

```mermaid
flowchart TB
    USER[User/Candidate] -->|Login/Register| SYSTEM((Sākṣin<br/>Interview<br/>Platform))
    USER -->|Take Interview| SYSTEM
    USER -->|Chat with AI| SYSTEM
    
    SYSTEM -->|Results| USER
    SYSTEM -->|Feedback| USER
    SYSTEM -->|Reports| USER
    
    ADMIN[Administrator] -->|Manage System| SYSTEM
    SYSTEM -->|Analytics| ADMIN
    
    SYSTEM <-->|AI Services| EXTERNAL[External Services<br/>Google Gemini<br/>Redis<br/>PostgreSQL]
    
    style USER fill:#fff,stroke:#000,stroke-width:4px,color:#000
    style SYSTEM fill:#fff,stroke:#000,stroke-width:4px,color:#000
    style ADMIN fill:#fff,stroke:#000,stroke-width:4px,color:#000
    style EXTERNAL fill:#fff,stroke:#000,stroke-width:3px,color:#000
```

---

## 5️⃣ UML Diagram - System Classes

```mermaid
classDiagram
    class User {
        +String username
        +String email
        +String password
        +String role
        +login()
        +register()
        +updateProfile()
    }
    
    class InterviewSession {
        +String sessionId
        +User user
        +String difficulty
        +String role
        +Date startTime
        +startInterview()
        +endInterview()
        +saveResponse()
    }
    
    class Question {
        +String questionId
        +String text
        +String difficulty
        +String category
        +generate()
        +validate()
    }
    
    class Response {
        +String responseId
        +String answer
        +Float score
        +Date timestamp
        +analyze()
        +calculateScore()
    }
    
    class AIService {
        +String modelName
        +generateQuestion()
        +analyzeResponse()
        +provideFeedback()
    }
    
    class Report {
        +String reportId
        +Float finalScore
        +String feedback
        +generate()
        +send()
    }
    
    User "1" --> "*" InterviewSession : takes
    InterviewSession "1" --> "*" Question : contains
    InterviewSession "1" --> "*" Response : collects
    Response "*" --> "1" Question : answers
    AIService "1" --> "*" Question : generates
    AIService "1" --> "*" Response : analyzes
    InterviewSession "1" --> "1" Report : produces
    
    style User fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style InterviewSession fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style Question fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style Response fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style AIService fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style Report fill:#fff,stroke:#000,stroke-width:2px,color:#000
```

---

## 6️⃣ ER Diagram - Database Schema

```mermaid
erDiagram
    USER ||--o{ INTERVIEW_SESSION : participates
    USER {
        int id PK
        string username
        string email
        string password_hash
        string role
        datetime created_at
    }
    
    INTERVIEW_SESSION ||--o{ QUESTION : contains
    INTERVIEW_SESSION ||--o{ RESPONSE : has
    INTERVIEW_SESSION ||--|| REPORT : generates
    INTERVIEW_SESSION {
        int id PK
        int user_id FK
        string session_id
        string difficulty
        string role
        datetime start_time
        datetime end_time
        string status
    }
    
    QUESTION ||--o{ RESPONSE : receives
    QUESTION {
        int id PK
        int session_id FK
        string question_text
        string category
        string difficulty
        int order_number
    }
    
    RESPONSE {
        int id PK
        int session_id FK
        int question_id FK
        text answer
        float score
        text feedback
        datetime answered_at
    }
    
    REPORT {
        int id PK
        int session_id FK
        float final_score
        text overall_feedback
        text strengths
        text weaknesses
        datetime generated_at
    }
    
    USER ||--o{ SUBSCRIPTION : has
    SUBSCRIPTION {
        int id PK
        int user_id FK
        string plan_type
        datetime start_date
        datetime end_date
        boolean active
    }
```

---

## 7️⃣ Activity Diagram - Interview Flow

```mermaid
flowchart TB
    START([User Starts Interview]) --> LOGIN{Logged In?}
    LOGIN -->|No| REG[Register/Login]
    REG --> LOGIN
    LOGIN -->|Yes| SELECT[Select Interview Type]
    
    SELECT --> CONFIG[Configure:<br/>Role, Experience,<br/>Difficulty]
    CONFIG --> INIT[Initialize Session]
    INIT --> LOAD[Load First Question]
    
    LOAD --> DISPLAY[Display Question]
    DISPLAY --> WAIT[Wait for Response]
    WAIT --> SUBMIT[User Submits Answer]
    
    SUBMIT --> ANALYZE[AI Analyzes Response]
    ANALYZE --> SCORE[Calculate Score]
    SCORE --> FEEDBACK[Generate Feedback]
    
    FEEDBACK --> SAVE[Save to Database]
    SAVE --> CACHE[Cache in Redis]
    
    CACHE --> CHECK{More Questions?}
    CHECK -->|Yes| NEXT[Load Next Question]
    NEXT --> DISPLAY
    
    CHECK -->|No| EVALUATE[Final Evaluation]
    EVALUATE --> REPORT[Generate Report]
    REPORT --> EMAIL[Send Email]
    REPORT --> SHOW[Display Results]
    
    SHOW --> ANALYTICS[Update Analytics]
    ANALYTICS --> END([End Session])
    
    style START fill:#fff,stroke:#000,stroke-width:3px,color:#000
    style LOGIN fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style REG fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style SELECT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style CONFIG fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style INIT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style LOAD fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style DISPLAY fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style WAIT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style SUBMIT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style ANALYZE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style SCORE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style FEEDBACK fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style SAVE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style CACHE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style CHECK fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style NEXT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style EVALUATE fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style REPORT fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style EMAIL fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style SHOW fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style ANALYTICS fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style END fill:#fff,stroke:#000,stroke-width:3px,color:#000
```

---

## 8️⃣ Sequence Diagram - Interview Process

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend API
    participant AI as Gemini AI
    participant R as Redis Cache
    participant D as Database
    
    U->>F: Click "Start Interview"
    F->>B: POST /api/interview/start
    B->>D: Create Session
    D-->>B: Session ID
    B->>R: Cache Session
    B-->>F: Return Session Details
    F-->>U: Show First Question
    
    U->>F: Submit Answer
    F->>B: POST /api/interview/answer
    B->>R: Get Session Context
    R-->>B: Session Data
    
    B->>AI: Analyze Response
    AI-->>B: Evaluation Result
    
    B->>D: Save Response & Score
    B->>R: Update Session Cache
    
    alt More Questions
        B-->>F: Next Question
        F-->>U: Display Question
    else Interview Complete
        B->>AI: Generate Final Report
        AI-->>B: Report Data
        B->>D: Save Report
        B-->>F: Final Results
        F-->>U: Show Results & Feedback
    end
```

---

## 9️⃣ Class Diagram - Detailed System Architecture

```mermaid
classDiagram
    class BaseModel {
        +DateTime created_at
        +DateTime updated_at
        +Boolean is_active
        +save()
        +delete()
    }
    
    class User {
        +String username
        +String email
        +String password_hash
        +String role
        +String experience
        +login()
        +logout()
        +updateProfile()
        +changePassword()
    }
    
    class InterviewSession {
        +UUID session_id
        +User user
        +String status
        +String difficulty
        +String role
        +Integer total_questions
        +Integer questions_answered
        +startSession()
        +endSession()
        +pauseSession()
        +getProgress()
    }
    
    class Question {
        +UUID question_id
        +String text
        +String category
        +String difficulty
        +Integer order
        +List expected_keywords
        +generateQuestion()
        +validateAnswer()
        +getHints()
    }
    
    class Response {
        +UUID response_id
        +Question question
        +Text answer
        +Float score
        +Text feedback
        +Integer time_taken
        +analyzeResponse()
        +calculateScore()
        +generateFeedback()
    }
    
    class GeminiAIClient {
        +String api_key
        +String model
        +Float temperature
        +generateContent()
        +analyzeText()
        +chat()
    }
    
    class ChatService {
        +String conversation_id
        +List messages
        +sendMessage()
        +getHistory()
        +clearConversation()
    }
    
    class InterviewService {
        +startInterview()
        +submitAnswer()
        +getNextQuestion()
        +calculateFinalScore()
    }
    
    class AnalyticsService {
        +getUserStats()
        +getPerformanceTrends()
        +generateInsights()
    }
    
    class Report {
        +UUID report_id
        +Float final_score
        +Text strengths
        +Text weaknesses
        +Text recommendations
        +List skill_scores
        +generate()
        +exportPDF()
        +sendEmail()
    }
    
    class Subscription {
        +String plan_type
        +DateTime start_date
        +DateTime end_date
        +Boolean auto_renew
        +upgrade()
        +cancel()
    }
    
    BaseModel <|-- User
    BaseModel <|-- InterviewSession
    BaseModel <|-- Question
    BaseModel <|-- Response
    BaseModel <|-- Report
    BaseModel <|-- Subscription
    
    User "1" --> "*" InterviewSession
    User "1" --> "0..1" Subscription
    InterviewSession "1" --> "*" Question
    InterviewSession "1" --> "*" Response
    InterviewSession "1" --> "1" Report
    Question "1" --> "*" Response
    
    GeminiAIClient "1" --> "*" Question : generates
    GeminiAIClient "1" --> "*" Response : analyzes
    ChatService --> GeminiAIClient : uses
    InterviewService --> GeminiAIClient : uses
    AnalyticsService --> InterviewSession : analyzes
    
    style BaseModel fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style User fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style InterviewSession fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style Question fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style Response fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style GeminiAIClient fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style ChatService fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style InterviewService fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style AnalyticsService fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style Report fill:#fff,stroke:#000,stroke-width:2px,color:#000
    style Subscription fill:#fff,stroke:#000,stroke-width:2px,color:#000
```

---

## 🖨️ Printing Instructions

### For A4 Paper Printing:

1. **Using Mermaid Live Editor:**
   - Go to https://mermaid.live/
   - Copy each diagram code
   - Click "Export" → "PNG" or "SVG"
   - Print with these settings:
     - Paper: A4
     - Orientation: Landscape (recommended)
     - Margins: Normal
     - Scale: Fit to page

2. **Using Markdown Preview:**
   - Open this file in VS Code
   - Use Markdown Preview Enhanced extension
   - Right-click → "Chrome (Puppeteer)" → "Export to PDF"
   - Print the PDF

3. **Using GitHub/GitLab:**
   - Push this file to your repository
   - View on GitHub/GitLab (they render Mermaid automatically)
   - Use browser's print function with:
     - Background graphics: ON
     - Scale: 90-100%

4. **Direct Browser Print:**
   - Open in browser with Mermaid support
   - Ctrl+P (Windows) / Cmd+P (Mac)
   - Enable "Background graphics"
   - Select A4 paper size

### Recommended Print Settings:
- **Paper Size:** A4 (210mm × 297mm)
- **Orientation:** Landscape for complex diagrams, Portrait for simple ones
- **Quality:** High/Best
- **Color:** Black & White (to save ink)
- **Margins:** 10mm all sides
- **Scale:** 90-95% (to avoid cutting edges)

---

**Created for:** Sākṣin AI-Powered Interview Platform  
**Date:** October 28, 2025  
**Version:** 1.0
