# Gemini File Search Starter 🔍

A complete, production-ready demo web application that enables users to upload documents (PDFs, DOCX, TXT, JSON, code files) and ask questions using Google's **Gemini 2.0 Flash with File Search** capabilities. Get AI-powered answers with citations directly from your uploaded files.

## ✨ Features

- **📁 File Upload**: Support for PDF, DOCX, TXT, JSON, and code files (.py, .js, .ts, .java, etc.)
- **🤖 AI-Powered Search**: Uses Gemini 2.0 Flash with File Search Store for semantic search
- **💬 Chat Interface**: Intuitive chat-style Q&A with your documents
- **📚 Citations**: Get grounded answers with source citations and snippets
- **🎨 Syntax Highlighting**: Code snippets from source files are automatically highlighted
- **🌙 Dark Mode**: Beautiful dark theme enabled by default
- **⚡ Real-time Status**: See upload and indexing status in real-time
- **🔒 Type-Safe**: Full TypeScript frontend with Zod validation
- **🐍 Python Backend**: FastAPI backend with comprehensive error handling

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Frontend - Next.js 15"
        A[User Interface]
        B[File Upload Component]
        C[Chat Interface]
        D[API Client with Zod]
    end
    
    subgraph "Backend - FastAPI"
        E[/upload Endpoint]
        F[/query Endpoint]
        G[/stores/list Endpoint]
        H[/stores/delete Endpoint]
        I[Gemini Client Wrapper]
    end
    
    subgraph "Google AI"
        J[Gemini 2.0 Flash Model]
        K[File Search Store]
        L[Vector Search Index]
    end
    
    subgraph "Storage"
        M[(Local Uploads)]
    end
    
    A --> B
    A --> C
    B --> D
    C --> D
    D --> E
    D --> F
    D --> G
    D --> H
    
    E --> I
    F --> I
    G --> I
    H --> I
    
    I --> J
    I --> K
    K --> L
    
    E --> M
    
    style A fill:#3b82f6
    style J fill:#10b981
    style K fill:#10b981
```

## 🚀 How File Search Works

Google's **Gemini File Search** provides powerful document understanding capabilities:

1. **Upload**: Files are uploaded to a File Search Store, which is a managed vector database
2. **Indexing**: Gemini automatically extracts text, creates embeddings, and indexes the content
3. **Query**: When you ask a question, the File Search tool:
   - Converts your query to embeddings
   - Performs semantic search across indexed documents
   - Retrieves relevant chunks
   - Uses Gemini to generate a grounded answer with citations
4. **Citations**: The response includes specific text snippets and source references

This approach provides:
- ✅ Semantic understanding (not just keyword matching)
- ✅ Context-aware answers
- ✅ Source attribution and transparency
- ✅ Support for multiple file formats

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+** 
- **Google AI API Key** (get one at [Google AI Studio](https://aistudio.google.com/app/apikey))

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/EdisonTKPcom/gemini-file-search-starter.git
cd gemini-file-search-starter
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your Google API Key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Set Up Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# The default API URL (http://localhost:8000) should work
```

## 🎯 Quick Start

### Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

The API will start at `http://localhost:8000`

### Start the Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

The web app will start at `http://localhost:3000`

### Open Your Browser

Navigate to `http://localhost:3000` and start uploading files!

## 📖 API Documentation

Once the backend is running, visit:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### `POST /upload`
Upload a file to a File Search Store.

**Form Data:**
- `file`: The file to upload
- `create_new_store`: Boolean to create a new store (optional)
- `store_name`: Existing store name to upload to (optional)

**Response:**
```json
{
  "success": true,
  "message": "File 'document.pdf' uploaded successfully",
  "file_info": {
    "name": "document.pdf",
    "file_id": "files/abc123",
    "status": "ready",
    "uploaded_at": "2024-01-15T10:30:00"
  },
  "store_name": "file_search_stores/xyz789"
}
```

#### `POST /query`
Query files in a File Search Store.

**Request Body:**
```json
{
  "query": "What is artificial intelligence?",
  "store_name": "file_search_stores/xyz789",
  "temperature": 0.1
}
```

**Response:**
```json
{
  "answer": "Artificial Intelligence (AI) is a branch of computer science...",
  "citations": [
    {
      "text": "AI is a branch of computer science that aims to create intelligent machines",
      "source": "ai_introduction.txt",
      "uri": "file://ai_introduction.txt"
    }
  ]
}
```

#### `GET /stores/list`
List all File Search Stores.

#### `DELETE /stores/{store_id}`
Delete a File Search Store.

## 💡 Example Queries

Once you've uploaded the sample files from the `examples/` folder, try these questions:

1. **About AI concepts:**
   - "What is the difference between narrow AI and general AI?"
   - "When was the term 'Artificial Intelligence' coined?"
   - "What are the ethical considerations of AI?"

2. **About the company data:**
   - "How many employees work in the Engineering department?"
   - "What is Bob Smith's position?"
   - "What projects are currently in progress?"

3. **About the code:**
   - "Explain how the fibonacci function works"
   - "What's the difference between the recursive and iterative implementations?"

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

With coverage:

```bash
pytest --cov=. --cov-report=html
```

## 📁 Project Structure

```
gemini-file-search-starter/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── gemini_client.py        # Gemini API wrapper
│   ├── test_main.py           # API endpoint tests
│   ├── test_gemini_client.py  # Client tests
│   ├── requirements.txt        # Python dependencies
│   ├── requirements-dev.txt    # Dev dependencies
│   ├── .env.example           # Environment template
│   └── .gitignore
├── frontend/
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Main dashboard
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   └── ui/                # shadcn/ui components
│   ├── lib/
│   │   ├── api-client.ts      # API client
│   │   ├── api-types.ts       # Zod schemas
│   │   └── utils.ts           # Utilities
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── .env.example
│   └── .gitignore
├── examples/
│   ├── ai_introduction.txt    # Sample text file
│   ├── company_data.json      # Sample JSON
│   ├── sample_code.py         # Sample code
│   └── demo_usage.py          # Usage script
└── README.md
```

## 🔧 Configuration

### Backend (.env)

```bash
GOOGLE_API_KEY=your_google_api_key_here
PORT=8000
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🌐 Deployment

### Backend Deployment

The backend can be deployed to:
- **Google Cloud Run**
- **AWS Lambda** (with API Gateway)
- **Heroku**
- **Railway**
- **Any VPS** with Python support

For production, update storage to use **Google Cloud Storage** instead of local files.

### Frontend Deployment

Deploy the Next.js frontend to:
- **Vercel** (recommended)
- **Netlify**
- **Cloudflare Pages**

Update `NEXT_PUBLIC_API_URL` to point to your production backend.

## 🛡️ Security Notes

- **Never commit** your `.env` files with real API keys
- Use environment variables for all sensitive data
- Implement rate limiting in production
- Add authentication for production deployments
- Validate and sanitize all user inputs
- Set up CORS properly for your domain

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - feel free to use this project for learning or production.

## 🙏 Acknowledgments

- **Google AI** for the Gemini API and File Search capabilities
- **Vercel** for Next.js
- **FastAPI** for the excellent Python framework
- **shadcn/ui** for the beautiful UI components

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Documentation**: [Google AI Documentation](https://ai.google.dev/docs)
- **API Reference**: [Gemini API Reference](https://ai.google.dev/api)

## 🎓 Learn More

- [Gemini File Search Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

Built with ❤️ using Gemini, Next.js, and FastAPI