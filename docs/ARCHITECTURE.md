# RecruitIQ Architecture

## System Design


## Components

### Frontend Layer
- **React Application**: Single-page application (SPA)
- **State Management**: Zustand for global state
- **API Client**: Axios for HTTP requests
- **Styling**: TailwindCSS + custom components

### Backend Services

#### Authentication Service
- OAuth 2.0 integration
- JWT token management
- Role-Based Access Control (RBAC)

#### Candidate Service
- Candidate CRUD operations
- Resume upload and processing
- Candidate profile management

#### Matching Service
- Job-to-candidate matching
- Semantic similarity scoring
- Match ranking and explanation

#### Analytics Service
- Hiring funnel metrics
- Bias audit reporting
- Recruiter activity tracking
- Salary intelligence

### AI Agent System

#### Resume Agent
- PDF/document parsing
- Skill extraction
- Experience analysis
- Education verification

#### Matching Agent
- Semantic similarity matching
- Score calculation
- Ranking algorithms
- Match explanation

#### Bias Agent
- Gender bias detection
- Educational bias analysis
- Geographic bias assessment
- Compliance reporting

#### Salary Agent
- Market salary analysis
- Location-based adjustments
- Experience-based estimation
- Negotiation insights

#### Email Agent
- Candidate communication
- Templated messaging
- Bulk outreach
- Follow-up automation

#### Interview Agent
- Question generation
- Candidate-specific customization
- Difficulty level adjustment
- Assessment rubrics

### Data Layer

#### PostgreSQL
- Relational data storage
- ACID compliance
- Vector support (pgvector)

#### Redis
- Session caching
- Job queue management
- Rate limiting
- Real-time notifications

#### Vector Database
- Resume embeddings
- Job description embeddings
- Semantic search capability

### External Services

#### AWS Services
- **S3**: Resume file storage
- **CloudFront**: CDN for frontend
- **ECS Fargate**: Container orchestration
- **RDS**: Managed PostgreSQL
- **Secrets Manager**: Credential storage
- **CloudWatch**: Monitoring and logging

#### Third-party APIs
- **OpenAI**: LLM for agent reasoning
- **HuggingFace**: Embedding models
- **Salary APIs**: Market data

## Data Flow

### Resume Analysis Flow
1. Recruiter uploads resume via frontend
2. File stored in S3
3. Resume Agent triggers extraction
4. Skills and experience extracted
5. Embeddings generated
6. Stored in vector DB
7. Results returned to frontend

### Matching Flow
1. Job requirements provided
2. Job embedding generated
3. Matching Agent queries vector DB
4. Similar resume vectors retrieved
5. Scoring and ranking applied
6. Bias audit performed
7. Results with explanations displayed

## Scalability Considerations

### Horizontal Scaling
- Stateless backend services
- Load balancing via Kubernetes
- Database replication
- Redis cluster mode

### Vertical Scaling
- CPU/memory allocation per pod
- Resource requests and limits
- Autoscaling policies

### Caching Strategy
- Redis for hot data
- CDN for static assets
- Query result caching
- Session caching

## Security Architecture

### Authentication & Authorization
- OAuth 2.0 for login
- JWT for API authentication
- RBAC for authorization
- Session management

### Data Protection
- HTTPS/TLS encryption
- At-rest encryption
- Secret management
- PII handling compliance

### API Security
- Rate limiting
- Input validation
- CORS configuration
- SQL injection prevention

## Monitoring & Observability

### Metrics
- Request latency
- Error rates
- AI agent performance
- Resume processing time

### Logging
- Structured logging
- ELK stack integration
- Request tracing
- Audit logging

### Alerting
- Error spike detection
- SLA monitoring
- Resource utilization alerts
- Security events


