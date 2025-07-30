# 📄 PDF Summary AI

A powerful web application for uploading large PDF files (up to 100 pages, 50MB) and receiving concise AI-generated summaries using OpenAI API.

## 🚀 Features

- **📤 PDF Upload**: Users can easily upload PDF files via drag & drop or file browser
- **🔍 Comprehensive PDF Parsing**: Accurate content extraction from PDFs with full support for text, images, and complex tables
- **🤖 AI Summarization**: Integration with OpenAI API to generate high-quality summaries of uploaded documents
- **📚 Recent History**: Display of the last 5 processed PDFs with key metadata and summary viewing capability

## 🛠 Technology Stack

### Backend

- **FastAPI** - Modern, fast web framework for Python
- **OpenAI API** - For AI summary generation
- **PyPDF2, PyMuPDF, pdfplumber** - For PDF parsing
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Typed JavaScript for better development experience
- **Vite** - Fast build tool and development server
- **Composables** - Clean composition API patterns

### DevOps

- **Docker** - Application containerization
- **Nginx** - Web server for frontend
- **Docker Compose** - Service orchestration

## 📋 Prerequisites

- Docker and Docker Compose
- OpenAI API key

## 🚀 Quick Start

### 1. Clone Repository

\`\`\`bash
git clone <repository-url>
cd cotix_test
\`\`\`

### 2. Environment Setup

\`\`\`bash

# Copy environment file and add your OpenAI API key

cp .env.example .env

# Edit .env file with your OPENAI_API_KEY

\`\`\`

### 3. Run with Docker Compose

\`\`\`bash

# Build and start all services

docker-compose up --build

# Or run in background

docker-compose up -d --build
\`\`\`

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Development

### Backend Development

\`\`\`bash
cd backend

# Create virtual environment

python -m venv venv
source venv/bin/activate # Linux/Mac

# or

venv\\Scripts\\activate # Windows

# Install dependencies

pip install -r requirements.txt

# Run development server

uvicorn app:app --reload --host 0.0.0.0 --port 8000
\`\`\`

### Frontend Development

\`\`\`bash
cd frontend

# Install dependencies

npm install

# Run development server

npm run dev

# Build for production

npm run build

# Format code

npm run format
\`\`\`

## 📡 API Endpoints

### POST /upload

Upload PDF file for processing

- **Request Body**: MultipartForm with file
- **Response**: File metadata and AI summary

### GET /history

Retrieve last 5 processed PDFs

- **Response**: List of files with metadata

### GET /download/{summary_id}

Download AI summary by ID

- **Parameters**: summary_id (string)
- **Response**: Summary text

### GET /health

Server health check

- **Response**: Server status

## 🐳 Docker Commands

\`\`\`bash

# Build images

docker-compose build

# Start services

docker-compose up

# Run in background

docker-compose up -d

# Stop services

docker-compose down

# View logs

docker-compose logs -f

# Clean rebuild

docker-compose down -v
docker-compose up --build
\`\`\`

## 📁 Project Structure

\`\`\`
cotix_test/
├── backend/ # FastAPI backend
│ ├── src/ # Source code
│ │ ├── api/ # API routes
│ │ ├── services/ # Business logic
│ │ ├── config.py # Configuration
│ │ ├── models.py # Data models
│ │ └── exceptions.py # Custom exceptions
│ ├── app.py # Main application
│ ├── requirements.txt # Python dependencies
│ ├── Dockerfile # Docker image for backend
│ ├── .env # Environment variables
│ └── .env.example # Environment template
├── frontend/ # Vue.js frontend
│ ├── src/
│ │ ├── components/ # Vue components
│ │ ├── composables/ # Composition API logic
│ │ ├── utils/ # Utility functions
│ │ ├── App.vue # Main component
│ │ ├── main.ts # Entry point
│ │ └── style.css # Global styles
│ ├── package.json # Node.js dependencies
│ ├── Dockerfile # Docker image for frontend
│ ├── nginx.conf # Nginx configuration
│ └── vite.config.ts # Vite configuration
├── storage/ # File storage
│ ├── pdfs/ # Uploaded PDF files
│ ├── summaries/ # Generated summaries
│ └── meta/ # File metadata
├── docker-compose.yml # Docker orchestration
├── .env # Global environment variables
└── README.md # Project documentation
\`\`\`

## 🏗 Architecture Principles

### Backend (SOLID Principles Applied)

- **Single Responsibility**: Each service handles one specific domain
- **Open/Closed**: Easy to extend with new file types or AI providers
- **Liskov Substitution**: Interface-based design for services
- **Interface Segregation**: Focused, specific interfaces
- **Dependency Inversion**: Dependency injection for testability

### Frontend (Clean Architecture)

- **Composables**: Reusable business logic
- **Separation of Concerns**: UI, API, and utilities clearly separated
- **Type Safety**: Full TypeScript implementation
- **DRY Principle**: Utility functions for common operations

## 🔒 Security Features

- CORS configured for allowed domains
- File type validation (PDF only)
- File size limits (50MB maximum)
- Page count limits (100 pages maximum)
- Input sanitization and validation

## 🚨 Troubleshooting

### OpenAI API Issues

- Verify your API key is correct
- Check your OpenAI account quotas
- Ensure access to GPT-4o-mini model

### Docker Issues

\`\`\`bash

# Clean Docker cache

docker system prune -a

# Recreate volumes

docker-compose down -v
docker volume prune
\`\`\`

### PDF Parsing Issues

- Ensure PDF is not password protected
- File must be a valid PDF format
- File size must not exceed 50MB

## 📊 Performance

- **Backend**: Async processing with FastAPI
- **Frontend**: Optimized build with Vite
- **Docker**: Multi-stage builds for smaller images
- **Caching**: Nginx static file caching

## 📝 License

This project was created for COXIT technical assessment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions, please create an issue in this repository.
