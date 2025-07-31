# PDF Summary AI

AI-powered PDF summarization service that processes large PDF files (up to 100 pages, 50MB) and generates concise summaries using OpenAI API.

## Features

- **PDF Upload**: Drag & drop or file browser upload with duplicate detection
- **AI Summarization**: OpenAI-powered content analysis and summary generation
- **Content Analysis**: Extracts text, images, and tables from PDFs
- **History**: Auto-refreshing list of recent uploads with original filenames
- **Real-time Processing**: Live progress tracking and status updates

## Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key

### Setup & Run

```bash
# Clone and setup
git clone https://github.com/iSevenpwnz/COXIT.git
cd cotix_test
cp .env.example .env

# Add your OpenAI API key to .env
OPENAI_API_KEY=your-key-here

# Start application
docker-compose up --build -d

 Access at http://localhost:5173
```

## Development

### Backend (FastAPI + Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Frontend (Vue 3 + TypeScript)

```bash
cd frontend
npm install
npm run dev  # Development server on port 5173
npm run build  # Production build
```

### Testing

```bash
# Backend tests
cd backend && python -m pytest

# Frontend tests
cd frontend && npm run test
```

## API Endpoints

| Method | Endpoint         | Description                 |
| ------ | ---------------- | --------------------------- |
| `POST` | `/upload`        | Upload PDF for processing   |
| `GET`  | `/history`       | Get recent uploads (last 5) |
| `GET`  | `/download/{id}` | Download summary by ID      |
| `GET`  | `/health`        | Service health check        |

## Project Structure

```
├── backend/           # FastAPI application
│   ├── src/
│   │   ├── api/       # Route handlers
│   │   ├── services/  # Business logic (PDF, AI, Storage)
│   │   ├── models.py  # Pydantic data models
│   │   └── config.py  # Application settings
│   ├── tests/         # Unit tests
│   └── app.py         # Main application
├── frontend/          # Vue 3 application
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── composables/    # Composition API logic
│   │   └── utils/          # Helper functions
│   ├── tests/         # Frontend tests
│   └── config/        # Build & deployment configs
├── storage/           # File storage (PDFs, summaries, metadata)
└── docker-compose.yml # Service orchestration
```

## Architecture

**Backend**: SOLID principles, service layer pattern, dependency injection
**Frontend**: Composition API, reactive state management, component-based architecture
**Testing**: Unit tests with >80% coverage, mocked dependencies
**Security**: File validation, size limits, CORS configuration, input sanitization

## Troubleshooting

**OpenAI Issues**: Verify API key and quota limits
**Docker Issues**: Run `docker-compose down -v && docker-compose up --build`  
**PDF Processing**: Ensure files are valid PDFs under 50MB, 100 pages

## License

Created for COXIT technical assessment.
