# Architecture Documentation

## System Overview

The Gemini File Search Starter is a full-stack web application that enables users to upload documents and query them using Google's Gemini AI with semantic search capabilities.

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui (Radix UI primitives)
- **State Management**: React Hooks (useState)
- **Type Validation**: Zod schemas
- **Syntax Highlighting**: react-syntax-highlighter

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **AI Integration**: Google Gemini API (google-genai SDK)
- **Data Validation**: Pydantic models
- **Testing**: pytest, pytest-asyncio
- **CORS**: FastAPI CORS middleware

### External Services
- **Google Gemini 2.0 Flash**: LLM for content generation
- **Gemini Files API**: File upload and management

## Component Architecture

### Frontend Components

#### 1. Main Dashboard (`app/page.tsx`)
The primary UI component containing:
- File upload interface
- Uploaded files list with status
- Chat interface for Q&A
- Citation display with code syntax highlighting

**Key Features:**
- Real-time upload status tracking
- File type validation
- Error handling with toast notifications
- Responsive layout with Tailwind

#### 2. UI Components (`components/ui/`)
Reusable components built on Radix UI:
- `button.tsx`: Primary interaction buttons
- `input.tsx`: Form input fields
- `card.tsx`: Content containers
- `toast.tsx`: Notification system
- `label.tsx`: Form labels

#### 3. API Client (`lib/api-client.ts`)
Type-safe API communication layer:
- Request/response validation with Zod
- Error handling and custom APIError class
- Methods: uploadFile, queryFiles, listStores, deleteStore

#### 4. Type Definitions (`lib/api-types.ts`)
Zod schemas for:
- File upload responses
- Query requests/responses
- Store information
- Citations

### Backend Components

#### 1. FastAPI Application (`main.py`)
REST API with the following endpoints:

**Endpoints:**
- `GET /`: Health check
- `GET /health`: Detailed health status
- `POST /upload`: Upload file to Gemini
- `POST /query`: Query uploaded files
- `GET /stores/list`: List all stores
- `DELETE /stores/{store_id}`: Delete a store
- `GET /supported-types`: Get supported file types

**Middleware:**
- CORS for cross-origin requests
- Custom error handlers

#### 2. Gemini Client Wrapper (`gemini_client.py`)
Abstraction layer for Google Gemini API:

**Features:**
- Retry logic with exponential backoff
- File upload management
- Store creation and management
- Query with file context
- MIME type detection

**Key Methods:**
```python
create_file_search_store(display_name) -> Dict
upload_file_to_store(file_path, store_name, mime_type) -> File
query_with_file_search(query, store_name, file_names, temperature) -> Dict
list_stores() -> List[Dict]
delete_store(store_name) -> None
```

#### 3. Data Models
Pydantic models for request/response validation:
- `QueryRequest`: Query parameters
- `QueryResponse`: Answer with citations
- `FileInfo`: File metadata
- `StoreInfo`: Store metadata
- `UploadResponse`: Upload result

## Data Flow

### File Upload Flow

```
1. User selects file in browser
   ↓
2. Frontend validates file type
   ↓
3. POST /upload with FormData
   ↓
4. Backend saves file locally
   ↓
5. Backend uploads to Gemini Files API
   ↓
6. Backend returns file info + store name
   ↓
7. Frontend updates UI with file status
```

### Query Flow

```
1. User enters question
   ↓
2. Frontend sends POST /query
   ↓
3. Backend retrieves uploaded files
   ↓
4. Backend creates content parts (query + file URIs)
   ↓
5. Gemini generates answer with file context
   ↓
6. Backend extracts answer + citations
   ↓
7. Frontend displays answer
   ↓
8. Frontend renders citations (with code highlighting)
```

## File Processing

### Supported File Types
- **Documents**: PDF, DOCX, TXT, MD
- **Data**: JSON, YAML, YML, XML
- **Code**: .py, .js, .ts, .java, .cpp, .c, .go, .rs, etc.

### MIME Type Detection
The backend automatically detects MIME types based on file extensions using a predefined mapping in `gemini_client.py`.

### File Storage
- **Development**: Local filesystem (`backend/uploads/`)
- **Production**: Can be extended to use Google Cloud Storage

## AI Integration

### Gemini API Usage

**Model**: `gemini-2.0-flash-exp`

**Key Parameters:**
- `temperature`: 0.1 (deterministic responses)
- `contents`: Query text + file URIs
- `config`: Generation configuration

**Response Structure:**
```python
{
    "answer": "Generated answer text",
    "citations": [
        {
            "text": "Cited snippet",
            "source": "filename.txt",
            "uri": "file://path"
        }
    ]
}
```

### Citation Extraction
The backend parses the Gemini response to extract:
1. Main answer text from response parts
2. Grounding metadata with citations
3. Retrieved context chunks with source attribution

## Security Considerations

### API Key Management
- Stored in `.env` files (never committed)
- Required for both development and production
- Validated on client initialization

### Input Validation
- File type restrictions
- File size limits (configurable)
- Query text validation
- Pydantic/Zod schema validation

### Error Handling
- Try-catch blocks throughout
- Custom error types (APIError)
- Graceful degradation
- User-friendly error messages

## Testing Strategy

### Backend Tests
**Unit Tests** (`test_gemini_client.py`, `test_main.py`):
- Client initialization
- MIME type detection
- Store operations
- File upload
- Query operations
- API endpoints

**Test Coverage:**
- 20 tests passing
- Mock external API calls
- Test both success and failure cases

### Frontend (Manual Testing)
- File upload functionality
- Query submission
- Citation display
- Error handling
- Responsive design

## Deployment Architecture

### Development
```
Frontend (localhost:3000) → Backend (localhost:8000) → Gemini API
```

### Production Options

**Backend Deployment:**
- Google Cloud Run (recommended)
- AWS Lambda + API Gateway
- Heroku
- Railway
- Any VPS with Python support

**Frontend Deployment:**
- Vercel (recommended for Next.js)
- Netlify
- Cloudflare Pages

**Environment Variables:**
```bash
# Backend
GOOGLE_API_KEY=your_key
PORT=8000

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Performance Considerations

### Optimization Strategies
1. **File Upload**: Stream large files instead of loading into memory
2. **Caching**: Implement Redis for frequently accessed data
3. **Rate Limiting**: Protect API endpoints from abuse
4. **Connection Pooling**: Reuse HTTP connections to Gemini API
5. **CDN**: Serve static assets via CDN

### Scalability
- Stateless backend allows horizontal scaling
- File storage can move to object storage (GCS/S3)
- Database can be added for metadata and user management

## Monitoring & Logging

### Backend Logging
- Structured logging with Python `logging` module
- Log levels: INFO, WARNING, ERROR
- Request/response logging
- Error tracking

### Metrics to Monitor
- API response times
- File upload success rate
- Query processing time
- Error rates by endpoint
- Gemini API quota usage

## Future Enhancements

### Planned Features
1. **User Authentication**: Add email/password or OAuth
2. **File Management**: Delete, rename, organize files
3. **Conversation History**: Save and restore Q&A sessions
4. **Advanced Search**: Filter by file type, date, etc.
5. **Batch Processing**: Upload multiple files at once
6. **Export Results**: Download Q&A as PDF/Markdown
7. **Real File Search Store**: Integrate with Vertex AI RAG when available
8. **Streaming Responses**: Real-time answer generation
9. **Multi-language Support**: i18n for UI
10. **Analytics Dashboard**: Usage statistics

### Technical Debt
- Add database for persistent storage
- Implement proper user session management
- Add rate limiting
- Implement file size limits
- Add comprehensive integration tests
- Set up CI/CD pipeline

## Development Workflow

### Local Setup
1. Clone repository
2. Set up Python virtual environment
3. Install backend dependencies
4. Set up Node.js environment
5. Install frontend dependencies
6. Configure environment variables
7. Run backend: `python main.py`
8. Run frontend: `npm run dev`

### Code Quality
- TypeScript for type safety
- Pydantic for runtime validation
- ESLint for JavaScript/TypeScript linting
- pytest for Python testing
- Pre-commit hooks (recommended)

## API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

**Issue**: "GOOGLE_API_KEY must be set"
- **Solution**: Add your API key to `.env` file

**Issue**: "Module not found"
- **Solution**: Install dependencies with `pip install -r requirements.txt` or `npm install`

**Issue**: "CORS error"
- **Solution**: Ensure backend CORS is configured for your frontend URL

**Issue**: "File upload fails"
- **Solution**: Check file type is supported and file size is reasonable

## Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
