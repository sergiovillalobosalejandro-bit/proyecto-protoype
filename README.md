# Clinical Intervention Tracking System

A comprehensive system for tracking individual clinical interventions with couders in educational programs, built with **FastAPI** and modern web technologies.

## 🚀 **Features**

- **🔍 Individual Couder Clinical History**: Search by CC and view complete intervention history
- **🤖 AI-Powered Analysis**: Generate synthesis and mini-diagnoses using OpenAI integration
- **📊 Multi-Level Dashboard**: Navigate through sede → corte → clan → couder metrics
- **🎵 Audio Recording**: Record and transcribe interventions with validation
- **📈 Real-time Metrics**: Track progress, dropouts, and completion rates
- **📝 Clinical Records Management**: Complete intervention tracking with timestamps
- **🔐 Secure Authentication**: JWT-based authentication with role-based access
- **⚡ High Performance**: Optimized queries and connection pooling

## 🛠 **Technology Stack**

### **Backend (FastAPI)**
- **Framework**: FastAPI 0.104.1+ with Python 3.8+
- **Database**: PostgreSQL 12+ with SQLAlchemy 2.0+ ORM
- **Document Store**: MongoDB 4.4+ with PyMongo
- **Authentication**: JWT tokens with OAuth2
- **Validation**: Pydantic v2 schemas
- **AI Integration**: OpenAI GPT-4 API
- **File Storage**: Local filesystem with validation

### **Frontend**
- **Framework**: Vanilla JavaScript (ES6+)
- **Styling**: Modern CSS with responsive design
- **Audio**: Web Audio API for recording
- **Architecture**: Modular JavaScript with ES6 modules

### **Infrastructure**
- **Database Migrations**: Alembic
- **Logging**: Centralized logging system
- **Security**: Rate limiting, CORS, security headers
- **Performance**: Connection pooling, optimized queries

## 📋 **Prerequisites**

### **System Requirements**
- Python 3.8 or higher
- PostgreSQL 12 or higher
- MongoDB 4.4 or higher
- Node.js 16+ (for development tools)
- Git

### **API Keys Required**
- OpenAI API key (for AI features)
- Optional: Email service credentials (for notifications)

## 🚀 **Quick Start Guide**

### **1. Clone and Setup**
```bash
# Clone the repository
git clone <repository-url>
cd proyecto-int-def

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### **2. Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify FastAPI installation
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
```

### **3. Database Setup**

#### **PostgreSQL Setup**
```bash
# Create database
createdb clinical_interventions

# Create user (optional)
createuser clinical_user
psql -d clinical_interventions -c "ALTER USER clinical_user PASSWORD 'your_password';"
psql -d clinical_interventions -c "GRANT ALL PRIVILEGES ON DATABASE clinical_interventions TO clinical_user;"
```

#### **MongoDB Setup**
```bash
# Start MongoDB service
# Windows:
net start MongoDB
# macOS:
brew services start mongodb-community
# Linux:
sudo systemctl start mongod

# Create database (will be created automatically on first use)
```

### **4. Environment Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Required `.env` variables:**
```env
# Database URLs
DATABASE_URL=postgresql://username:password@localhost:5432/clinical_interventions
MONGODB_URL=mongodb://localhost:27017/clinical_records

# Security
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Integration
OPENAI_API_KEY=sk-your-openai-api-key-here

# CORS (for production)
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Security Settings
RATE_LIMIT_PER_MINUTE=100
MAX_AUDIO_FILE_SIZE_MB=50

# Logging
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_TO_CONSOLE=true
```

### **5. Database Initialization**
```bash
# Run complete setup (creates tables, indexes, sample data)
python scripts/setup_database.py

# Create MongoDB indexes for performance
python scripts/setup_mongodb_indexes.py

# Create admin user
python scripts/create_admin.py

# Or run complete optimization
python scripts/optimize_system.py
```

### **6. Start the Application**
```bash
# Start FastAPI development server
python run.py

# Or use uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **7. Access the Application**
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Frontend Application**: Open `frontend/index.html` in your browser
- **Health Check**: http://localhost:8000/health

### **8. Default Login**
- **Username**: `admin`
- **Password**: `admin123`

## 📚 **FastAPI Integration Details**

### **FastAPI Architecture**
The application follows FastAPI best practices:

#### **Dependency Injection**
```python
# Database dependencies
from app.core.database import get_db
from app.core.mongodb import get_mongo_db

# Usage in endpoints
@router.get("/couders/{couder_id}")
async def get_couder(couder_id: int, db: Session = Depends(get_db)):
    # Database operations
```

#### **Pydantic v2 Schemas**
```python
# Request/Response models with validation
class CouderCreate(BaseModel):
    cc: str
    nombre_completo: str
    
    @field_validator('cc')
    @classmethod
    def validate_cc(cls, v):
        if not re.match(r'^\d{6,12}$', v):
            raise ValueError('CC debe contener solo números (6-12 dígitos)')
        return v
```

#### **Response Models**
```python
# Typed responses with automatic documentation
@router.get("/couders/{couder_id}", response_model=CouderResponse)
async def get_couder(couder_id: int, db: Session = Depends(get_db)):
    # Returns validated response
```

#### **Status Codes**
```python
# Proper HTTP status codes
@router.post("/interventions", status_code=status.HTTP_201_CREATED)
async def create_intervention(intervention: IntervencionCreate):
    # Returns 201 Created
```

### **API Endpoints Structure**

#### **Authentication** (`/api/auth`)
- `POST /login` - User login
- `POST /register` - User registration
- `GET /me` - Current user info

#### **Couders** (`/api/couders`)
- `GET /search/{cc}` - Search by CC
- `GET /` - List couders with filters
- `POST /` - Create new couder
- `PUT /{id}` - Update couder
- `DELETE /{id}` - Soft delete couder

#### **Interventions** (`/api/intervenciones`)
- `GET /couder/{id}` - Get couder interventions
- `POST /` - Create intervention
- `PUT /{id}` - Update intervention
- `DELETE /{id}` - Delete intervention

#### **Dashboard** (`/api/dashboard`)
- `GET /overview` - Main metrics
- `GET /sedes/{id}` - Sede details
- `GET /cortes/{id}` - Corte details
- `GET /clanes/{id}` - Clan details

#### **AI Services** (`/api/ai`)
- `POST /synthesize/{id}` - Generate synthesis
- `POST /diagnose/{id}` - Generate diagnosis
- `GET /history/{id}` - AI analysis history

#### **Audio** (`/api/audio`)
- `POST /upload` - Upload audio recording
- `GET /{id}` - Get audio info
- `GET /{id}/download` - Download audio file
- `DELETE /{id}` - Delete audio

### **FastAPI Features Used**

#### **Automatic Documentation**
- Interactive Swagger UI at `/docs`
- ReDoc documentation at `/redoc`
- OpenAPI 3.0 specification

#### **Data Validation**
- Pydantic v2 models with field validators
- Automatic request/response validation
- Type hints for editor support

#### **Dependency Injection**
- Database session management
- MongoDB connection handling
- Authentication dependencies

#### **Security**
- OAuth2 with JWT tokens
- CORS middleware
- Rate limiting middleware
- Security headers

#### **Performance**
- Connection pooling
- Optimized database queries
- Async request handling

## 🔧 **Development**

### **Development Server**
```bash
# Start with auto-reload
uvicorn app.main:app --reload

# Enable SQL logging
uvicorn app.main:app --reload --log-level debug

# Custom host/port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### **Database Migrations**
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### **Testing**
```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/test_auth.py
```

### **Code Quality**
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## 📊 **Database Schema**

### **PostgreSQL Tables**
```
┌─────────────────┐
│     usuarios    │ ← Users and authentication
├─────────────────┤
│      sedes      │ ← Educational centers
├─────────────────┤
│     cortes      │ ← Time-based cohorts
├─────────────────┤
│     clanes      │ ← Subgroups (AM/PM)
├─────────────────┤
│    couders      │ ← Participants
├─────────────────┤
│ intervenciones  │ ← Intervention records
└─────────────────┘
```

### **MongoDB Collections**
```
┌─────────────────────┐
│ historial_clinico   │ ← Complete clinical records
├─────────────────────┤
│    ai_analisis      │ ← AI-generated analyses
├─────────────────────┤
│  audio_registros    │ ← Audio file metadata
├─────────────────────┤
│seguimiento_progreso │ ← Progress tracking
└─────────────────────┘
```

## 🎯 **User Guide**

### **Dashboard Navigation**
1. **Main Dashboard**: View overall metrics across all sedes
2. **Sede Details**: Click on any sede to see corte breakdown
3. **Corte Details**: View clans with AM/PM organization
4. **Clan Details**: See individual couder metrics

### **Clinical Workflow**
1. **Search Couder**: Use CC number to find participants
2. **View History**: Access complete clinical record
3. **Add Interventions**: Record new sessions with details
4. **AI Analysis**: Generate synthesis and diagnoses
5. **Audio Recording**: Capture and transcribe sessions

### **AI Features**
- **Synthesis**: Combines multiple interventions into comprehensive summary
- **Diagnosis**: Provides preliminary assessment based on history
- **Suggestions**: Offers specific recommendations for treatment
- **Risk Assessment**: Evaluates intervention urgency level

## 🔒 **Security**

### **Authentication**
- JWT-based authentication with configurable expiration
- Password hashing with bcrypt
- Role-based access control (Admin, Terapista, Coordinador)

### **Data Protection**
- Input validation and sanitization
- SQL injection prevention with SQLAlchemy
- File upload validation
- Rate limiting protection

### **Security Headers**
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

## 🚀 **Production Deployment**

### **Environment Setup**
```bash
# Production environment variables
export DATABASE_URL="postgresql://user:pass@prod-db:5432/clinical_interventions"
export MONGODB_URL="mongodb://prod-mongo:27017/clinical_records"
export SECRET_KEY="production-secret-key"
export ALLOWED_ORIGINS="https://yourdomain.com"
export LOG_LEVEL="WARNING"
```

### **Docker Deployment**
```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Docker Compose**
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/clinical_interventions
      - MONGODB_URL=mongodb://mongo:27017/clinical_records
    depends_on:
      - db
      - mongo
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=clinical_interventions
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
  
  mongo:
    image: mongo:4.4
```

### **Performance Optimization**
- Use connection pooling (configured)
- Enable database query caching
- Implement Redis for session storage
- Use CDN for static assets
- Enable gzip compression

### **Monitoring**
- Application logs in `logs/` directory
- Health check endpoint at `/health`
- Performance metrics collection
- Error tracking and alerting

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Database Connection**
```bash
# Check PostgreSQL
psql -h localhost -U postgres -d clinical_interventions

# Check MongoDB
mongo --eval "db.adminCommand('ismaster')"
```

#### **FastAPI Issues**
```bash
# Check FastAPI installation
python -c "import fastapi; print('FastAPI OK')"

# Check dependencies
pip check

# View detailed errors
uvicorn app.main:app --log-level debug
```

#### **Frontend Issues**
- Check browser console for JavaScript errors
- Verify API base URL in `frontend/js/config.js`
- Ensure CORS is properly configured

#### **AI Features**
- Verify OpenAI API key is valid
- Check internet connectivity
- Review OpenAI API usage limits

### **Logs**
```bash
# View application logs
tail -f logs/clinical_$(date +%Y%m%d).log

# View error logs
tail -f logs/errors_$(date +%Y%m%d).log

# View all logs
ls -la logs/
```

## 📈 **Performance Metrics**

### **Database Optimization**
- Connection pooling: 10 base connections, 20 max overflow
- Query optimization: Single dashboard query vs N+1 queries
- MongoDB indexes: Optimized for common query patterns

### **API Performance**
- Response time: <200ms for most endpoints
- Concurrent users: 100+ with rate limiting
- File upload: 50MB max with validation

### **Monitoring Endpoints**
- `/health` - Application health status
- `/metrics` - Performance metrics (if configured)
- Database query logs available in development

## 🤝 **Contributing**

### **Development Workflow**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with tests
4. Run quality checks: `black app/ && flake8 app/ && mypy app/`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open Pull Request

### **Code Standards**
- Follow PEP 8 for Python code
- Use type hints for all functions
- Write comprehensive docstrings
- Add tests for new features
- Update documentation

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 **Support**

### **Getting Help**
- 📖 **Documentation**: Check this README and API docs
- 🐛 **Issues**: Create an issue on GitHub
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Email**: Contact the development team

### **Resources**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Documentation](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MongoDB Documentation](https://docs.mongodb.com/)

---

## 🎉 **Ready to Start!**

1. **Clone** the repository
2. **Install** dependencies: `pip install -r requirements.txt`
3. **Configure** environment: `cp .env.example .env`
4. **Setup** databases: `python scripts/setup_database.py`
5. **Start** server: `python run.py`
6. **Access** at: `http://localhost:8000/docs`

**Built with ❤️ using FastAPI**
