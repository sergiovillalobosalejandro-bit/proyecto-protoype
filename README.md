# Clinical Intervention Tracking System

A comprehensive system for tracking individual clinical interventions with couders in educational programs.

## Features

- **Individual Couder Clinical History**: Search by CC and view complete intervention history
- **AI-Powered Analysis**: Generate synthesis and mini-diagnoses using OpenAI integration
- **Multi-Level Dashboard**: Navigate through sede → corte → clan → couder metrics
- **Audio Recording**: Record and transcribe interventions
- **Real-time Metrics**: Track progress, dropouts, and completion rates
- **Clinical Records Management**: Complete intervention tracking with timestamps

## Technology Stack

- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript with modern CSS
- **Databases**: PostgreSQL (relational data) + MongoDB (clinical documents)
- **AI**: OpenAI GPT-4 for analysis and synthesis
- **Authentication**: JWT-based secure authentication

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- MongoDB 4.4+
- Node.js (for development tools)

### Installation

1. **Clone and install dependencies**:
```bash
cd proyecto-int-def
pip install -r requirements.txt
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your database URLs and API keys
```

3. **Set up databases**:
```bash
python scripts/setup_database.py
```

4. **Start the backend server**:
```bash
python run.py
```

5. **Open the frontend**:
Open `frontend/index.html` in your web browser

### Default Login

- **Username**: `admin`
- **Password**: `admin123`

## Database Setup

### PostgreSQL

The system uses PostgreSQL for relational data including:
- Users and authentication
- Sedes, cortes, and clanes
- Couders and basic information
- Interventions metadata

### MongoDB

MongoDB stores clinical documents:
- Complete clinical history records
- AI-generated analyses and suggestions
- Audio recording metadata and transcriptions
- Progress tracking data

### Schema Overview

```
PostgreSQL Tables:
├── usuarios (users)
├── sedes (educational centers)
├── cortes (time-based cohorts)
├── clanes (subgroups)
├── couders (participants)
└── intervenciones (interventions)

MongoDB Collections:
├── historial_clinico (clinical records)
├── ai_analisis (AI analyses)
├── audio_registros (audio recordings)
└── seguimiento_progreso (progress tracking)
```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Main Endpoints

- **Authentication**: `/api/auth/*`
- **Couders**: `/api/couders/*`
- **Interventions**: `/api/intervenciones/*`
- **Dashboard**: `/api/dashboard/*`
- **AI Services**: `/api/ai/*`
- **Audio**: `/api/audio/*`

## Frontend Structure

The frontend is built with vanilla JavaScript and includes:

- **Dashboard View**: Multi-level metrics and navigation
- **Search View**: Find couders by CC number
- **Clinical View**: Complete history management
- **AI Integration**: Synthesis and diagnosis generation
- **Audio Recording**: Browser-based audio capture

## Configuration

### Environment Variables

```env
DATABASE_URL=postgresql://username:password@localhost:5432/clinical_interventions
MONGODB_URL=mongodb://localhost:27017/clinical_records
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key
```

### AI Integration

To enable AI features:
1. Get an OpenAI API key
2. Set `OPENAI_API_KEY` in your environment
3. The system will use GPT-4 for synthesis and diagnosis

## Development

### Project Structure

```
proyecto-int-def/
├── app/                    # Backend application
│   ├── api/               # API routers
│   ├── core/              # Core configuration
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── frontend/              # Frontend application
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript modules
│   └── index.html        # Main HTML file
├── scripts/              # Utility scripts
├── backend/database/     # Database schemas
└── alembic/             # Database migrations
```

### Running Tests

```bash
# Run backend tests
python -m pytest

# Run with coverage
python -m pytest --cov=app
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## User Guide

### Dashboard Navigation

1. **Main Dashboard**: View overall metrics across all sedes
2. **Sede Details**: Click on any sede to see corte breakdown
3. **Corte Details**: View clans with AM/PM organization
4. **Clan Details**: See individual couder metrics

### Clinical Workflow

1. **Search Couder**: Use CC number to find participants
2. **View History**: Access complete clinical record
3. **Add Interventions**: Record new sessions with details
4. **AI Analysis**: Generate synthesis and diagnoses
5. **Audio Recording**: Capture and transcribe sessions

### AI Features

- **Synthesis**: Combines multiple interventions into comprehensive summary
- **Diagnosis**: Provides preliminary assessment based on history
- **Suggestions**: Offers specific recommendations for treatment
- **Risk Assessment**: Evaluates intervention urgency level

## Security

- JWT-based authentication with configurable expiration
- Password hashing with bcrypt
- Role-based access control (Admin, Terapista, Coordinador)
- Secure file upload handling for audio
- HIPAA-style data protection for clinical information

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure PostgreSQL and MongoDB are running
2. **AI Features**: Check OpenAI API key configuration
3. **Audio Recording**: Browser may require HTTPS for microphone access
4. **CORS Issues**: Configure appropriate origins in production

### Logs

Check the server logs for detailed error information:
```bash
python run.py --log-level debug
```

## Production Deployment

### Environment Setup

1. Use environment variables for all configuration
2. Enable HTTPS with valid SSL certificates
3. Configure proper database backups
4. Set up monitoring and logging
5. Use production-grade database servers

### Security Considerations

- Change default admin password
- Use strong secret keys
- Enable database encryption
- Configure firewall rules
- Regular security updates

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation wiki
