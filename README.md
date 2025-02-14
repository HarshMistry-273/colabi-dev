# Colabi Project

Colabi is a FastAPI-based project that integrates LangChain, CrewAI, and Celery for handling AI-powered tasks and background processing. This README provides comprehensive setup and usage instructions.

## Features

- FastAPI backend with automatic API documentation
- Celery integration for background task processing
- LangChain and CrewAI integration for AI operations
- Docker support for easy deployment
- MySQL database with Alembic migrations
- Redis for message broker and caching
- Comprehensive testing setup

## Prerequisites

- Python 3.12.0
- Docker and Docker Compose (for containerized deployment)
- pip (Python package installer)
- Git

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── main.py
├── alembic/
│   ├── versions/
│   └── env.py
├── alembic.ini
├── database/
│   ├── __init__.py
├── src/
│   ├── __init__.py
│   ├── celery.py
│   ├── app.py
│   ├── config.py
│   ├── preprocessing.py
│   ├── agents/
│   ├── crew_agents/
│   ├── tasks/
│   ├── tools/
│   └── utils/
├── .env.example
├── requirements.txt
└── README.md
```

## Installation & Setup

### Option 1: Docker Deployment (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/colabi.git
cd colabi
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Update the .env file with your configurations and API keys

4. Build and start the Docker containers:
```bash
docker-compose up --build -d
```

5. Access the services:
- FastAPI application: http://localhost:8001/docs
- Redis: localhost:6379

6. Stop the services:
```bash
docker-compose down --remove-orphans
```

### Option 2: Local Development Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Start the FastAPI server:
```bash
python main.py
```

5. Start Celery worker:
```bash
# Windows
celery -A src.celery worker --pool=solo -l info

# macOS/Linux
celery -A src.celery worker -l info
```

## Database Management

### Initialize Alembic (First Time Setup)
```bash
alembic init alembic
```

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade to specific version
alembic upgrade <revision>

# Downgrade to specific version
alembic downgrade <revision>
```

### View Migration History
```bash
alembic history --verbose
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8001/docs (Docker) or http://localhost:8000/docs (Local)
- ReDoc: http://localhost:8001/redoc (Docker) or http://localhost:8000/redoc (Local)

## Dependencies

Key dependencies include:

```
crewai==0.67.1
crewai-tools==0.12.1
langchain==0.2.16
langchain-community==0.2.17
python-dotenv==1.0.1
fastapi==0.115.0
PyMySQL==1.1.1
celery==5.4.0
redis==5.1.1
alembic==1.12.0
SQLAlchemy==2.0.23
```

For a complete list, see `requirements.txt`.

## Environment Variables

Key environment variables that need to be configured in `.env`:

```
# FastAPI Settings
APP_NAME=Colabi
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000

# Database Settings
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/colabi

# Redis Settings
REDIS_HOST=localhost
REDIS_PORT=6379

# API Keys
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

## Troubleshooting

### Common Issues

1. Database Connection Errors
   - Verify database credentials in .env
   - Ensure MySQL service is running
   - Check network connectivity

2. Redis Connection Issues
   - Verify Redis is running
   - Check Redis connection settings
   - Ensure proper network access

3. Celery Worker Problems
   - Verify Redis connection
   - Check Celery worker logs
   - Ensure proper task registration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request
