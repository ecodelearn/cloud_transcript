# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**cloud_transcript** evolved from a simple WhatsApp transcription tool into a **complete AI consultancy management platform**:

### **Phase 1** (Current): GPU-powered transcription with RTX 3060
### **Phase 2**: Project management for AI consultancy workflow  
### **Phase 3**: Cloud sync with Supabase + VPS deployment
### **Future**: Multi-tenant SaaS for consultants

**Core Workflow**: WhatsApp initial contact → Google Meet (2-4h) → AI analysis → Automated proposal generation

## Architecture

Based on the project specification in `NOVO_PROJETO_TRANSCRITOR.md`, this is a **Streamlit-based Python application** with the following structure:

```
cloud_transcript/
├── src/                          # Source code
│   ├── app.py                   # Main Streamlit interface
│   ├── config.py                # Application configuration
│   ├── models/                  # Database models & schemas
│   │   ├── database.py         # SQLite/Supabase connection
│   │   ├── project.py          # Project model
│   │   ├── meeting.py          # Meeting model
│   │   └── insight.py          # AI insights model
│   ├── services/
│   │   ├── whisper_gpu.py      # Local GPU Whisper processing
│   │   ├── transcription.py    # Multi-engine transcription
│   │   ├── audio_processor.py  # Audio segmentation & processing
│   │   ├── llm_analyzer.py     # AI insights extraction
│   │   └── export_manager.py   # Multiple format exports
│   ├── components/
│   │   ├── project_manager.py  # Project CRUD interface
│   │   ├── meeting_timeline.py # Meeting navigation
│   │   ├── audio_uploader.py   # Drag & drop upload
│   │   ├── transcription_viewer.py # Review/edit transcriptions
│   │   └── insights_panel.py   # AI analysis results
│   └── utils/
│       ├── file_utils.py       # File handling utilities
│       ├── database_utils.py   # Database helpers
│       └── format_utils.py     # Data formatting utilities
├── data/                         # Local data storage
│   ├── cloud_transcript.db     # SQLite database
│   ├── projects/               # Audio files organized by project
│   └── models/                 # Whisper model cache
├── docs/                        # Documentation & planning
│   ├── context/                # Context files for development
│   └── planning/               # Evolution, roadmap, database
│       ├── EVOLUTION.md        # Phased development plan
│       ├── DATABASE.md         # Database architecture
│       ├── ROADMAP.md          # Sprint planning
│       ├── AGENTS.md           # Development agents
│       └── ISSUES.md           # Task tracking
├── docker/                      # Docker configurations
├── deploy/                      # Deployment scripts (Supabase, VPS)
├── requirements.txt            # CPU dependencies
├── requirements.gpu.txt        # GPU dependencies
├── Dockerfile                  # CPU container
├── Dockerfile.gpu              # GPU container
├── docker-compose.yml          # CPU development
├── docker-compose.gpu.yml      # GPU development
├── .env.example               # Environment variables template
└── README.md
```

## Key Technologies

- **Docker & Docker Compose** for containerized development
- **Python 3.9+**
- **Streamlit** for web interface
- **Groq Python SDK** (primary transcription API)
- **pydub** for audio processing
- **streamlit-sortables** for drag & drop functionality
- **streamlit-ace** for text editing

## Core Data Structure

The application uses a `ConversationBlock` structure:
```python
ConversationBlock = {
    "id": str,
    "type": "audio" | "text",
    "content": str,
    "timestamp": datetime,
    "audio_file": str | None,
    "duration": float | None
}
```

## Development Commands

### Local Development with Docker
```bash
# Start the application locally
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f app

# Rebuild after changes
docker-compose up --build
```

### Environment Setup
1. Copy `.env.example` to `.env`
2. Configure API keys (GROQ_API_KEY, GOOGLE_CLOUD_KEY, etc.)
3. Run `docker-compose up --build`

## Application Workflow

1. **Upload Phase**: Multiple audio file upload (.opus, .mp3)
2. **Processing Phase**: Batch transcription via configured API
3. **Editing Phase**: Visual block editor for context insertion and reordering
4. **Export Phase**: Multiple format exports (TXT, JSON, Markdown, Chat format)

## API Integration Priority

1. **Groq** (Primary) - Whisper-large-v3 model, 6,000 seconds/minute free tier
2. **Google Cloud Speech-to-Text** (Secondary) - 60 minutes/month free tier
3. **Hugging Face Inference API** (Fallback) - Rate limited

## Key Features to Implement

- Drag & drop file upload interface
- Real-time transcription progress tracking
- Visual timeline of conversation blocks
- Inline editing of transcriptions
- Smart caching to avoid re-transcription
- Multiple export formats optimized for LLM consumption
- Automatic audio file ordering by timestamp/name

## Dependencies

Expected main dependencies:
```
streamlit
groq
pydub
streamlit-sortables
streamlit-ace
python-dotenv
```

## Deployment Architecture

### Local Development (Docker Compose)
- Single container running Streamlit app on port 8501
- Volume mounts for hot reloading during development
- Environment variables managed via .env file

### Production Deployment Options
1. **Google Cloud Run** - Serverless container deployment
2. **VPS** - Traditional server deployment with Docker

## Development Notes

- Project is designed for rapid prototyping (MVP in 2-3 hours)
- Focus on Portuguese (PT-BR) language support
- Implement retry logic for API failures
- Include comprehensive error handling for audio file processing
- Cache transcription results to improve performance
- Use Docker volumes for persistent data storage
- Environment-based configuration for different deployment targets
- to memorize