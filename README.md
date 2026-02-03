# Video RAG Chat System - Full Stack Application

A production-ready full-stack application for transcribing YouTube videos and asking questions using Retrieval-Augmented Generation (RAG).

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  React Frontend │ ◄────► │  FastAPI Backend │
│   (Port 3000)   │  REST   │   (Port 8000)    │
└─────────────────┘  API    └──────────────────┘
                                     │
                            ┌────────┴────────┐
                            │                 │
                        ┌───▼───┐      ┌──────▼──────┐
                        │OpenAI │      │Vector Store │
                        │GPT    │      │(In-Memory/  │
                        │Whisper│      │ Pinecone)   │
                        └───────┘      └─────────────┘
```

## 📁 Project Structure

```
rag_system/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py          # REST API endpoints
│   │   └── models.py          # Pydantic models
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Configuration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── embeddings_manager.py
│   │   ├── vector_store.py
│   │   └── llm_client.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── rag_pipeline.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── video_service.py   # Business logic
│   ├── main.py                # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.jsx
│   │   │   ├── VideoInput.jsx
│   │   │   └── SearchChunks.jsx
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- ffmpeg (required for Whisper)
- OpenAI API key

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# (Optional) Create .env file for custom API URL
cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000/api/v1
EOF

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## 🎯 Usage

### 1. Process a Video

1. Open `http://localhost:3000`
2. Enter a YouTube URL
3. Click "Process Video"
4. Wait for transcription (may take several minutes)

### 2. Ask Questions

1. Go to the "Chat" tab
2. Type your question
3. Get AI-generated answers based on video content

### 3. Search Chunks

1. Go to the "Search" tab
2. Enter search keywords
3. View relevant text sections

### 4. View Transcription

1. Go to the "Transcription" tab
2. See the full video transcription

## 📡 API Endpoints

### Video Processing

```http
POST /api/v1/video/process
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=..."
}
```

### Chat/Q&A

```http
POST /api/v1/chat
Content-Type: application/json

{
  "question": "What is the main topic?"
}
```

### Search Chunks

```http
POST /api/v1/search
Content-Type: application/json

{
  "query": "neural networks",
  "num_chunks": 3
}
```

### Get Transcription

```http
GET /api/v1/transcription
```

### Check Status

```http
GET /api/v1/status
```

## ⚙️ Configuration

### Backend Configuration

Edit `backend/config/settings.py`:

```python
# Model Settings
llm_model = "gpt-3.5-turbo"
embedding_model = "text-embedding-ada-002"
temperature = 0.0
max_tokens = 1000

# Chunking Settings
chunk_size = 1000
chunk_overlap = 20

# Vector Store Settings
store_type = "in_memory"  # or "pinecone"
top_k = 4
```

### Frontend Configuration

Edit `frontend/.env`:

```env
# API URL (default uses proxy to localhost:8000)
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 🔧 Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if implemented)
pytest

# Format code
black .

# Lint
flake8
```

### Frontend Development

```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## 🚢 Production Deployment

### Backend Deployment

```bash
# Build Docker image
cd backend
docker build -t video-rag-api .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  video-rag-api

# Or use gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment

```bash
cd frontend

# Build production bundle
npm run build

# Serve with nginx or deploy to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Any static hosting service
```

### Environment Variables (Production)

**Backend:**
```env
OPENAI_API_KEY=your_production_key
PINECONE_API_KEY=your_pinecone_key  # if using Pinecone
```

**Frontend:**
```env
REACT_APP_API_URL=https://api.yourdomain.com/api/v1
```

## 🔒 Security Considerations

1. **CORS**: Update `backend/main.py` to specify exact origins in production
2. **API Keys**: Never commit `.env` files to version control
3. **Rate Limiting**: Consider implementing rate limiting for API endpoints
4. **Authentication**: Add JWT authentication for production use
5. **HTTPS**: Always use HTTPS in production

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### API Testing

Use the interactive docs at `http://localhost:8000/docs` to test endpoints.

## 📊 Monitoring

- **Backend Logs**: Check console output or configure logging
- **Health Check**: `GET /health`
- **Status Endpoint**: `GET /api/v1/status`

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in main.py or:
uvicorn main:app --port 8001
```

**OpenAI API errors:**
- Check API key in `.env`
- Verify API quota/billing
- Check network connectivity

**ffmpeg not found:**
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings
- Verify `REACT_APP_API_URL` in `.env`

**Build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📧 Support

For issues and questions:
- Check the [API Documentation](http://localhost:8000/docs)
- Review this README
- Open an issue on GitHub

---

**Built with:** FastAPI • React • OpenAI GPT • Whisper • LangChain