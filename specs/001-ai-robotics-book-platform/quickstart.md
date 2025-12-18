# Quickstart Guide for AI & Robotics Book Platform

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.11 or higher)
- pip package manager
- Git

## Setting up the Development Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up the Backend
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration
```

### 3. Set up the Frontend
```bash
# Navigate to the frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration
```

## Environment Configuration

### Backend Environment Variables (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/robotics_book
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
GEMINI_API_KEY=AIzaSyB8LVwU_D6hq1rW5r7aSdC_9htU4LipJ00
JWT_SECRET=your-jwt-secret
AUTH_SECRET=your-auth-secret
```

### Frontend Environment Variables (.env)
```
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_AUTH_DOMAIN=your-auth-domain
```

## Running the Applications

### Backend (FastAPI server)
```bash
# From the backend directory
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the development server
uvicorn src.main:app --reload --port 8000
```

### Frontend (Docusaurus server)
```bash
# From the frontend directory
cd frontend

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

## Running Tests

### Backend Tests
```bash
# From the backend directory
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

### Frontend Tests
```bash
# From the frontend directory
cd frontend

# Run unit tests
npm test

# Run end-to-end tests (if Playwright is configured)
npx playwright test
```

## Setting up the Database

### Migrate the database (after environment is configured):
```bash
# From the backend directory
cd backend
source venv/bin/activate

# Run database migrations
python -m src.database.migrate
```

## Indexing Book Content for RAG

### To index all book chapters into the vector database:
```bash
# From the backend directory
cd backend
source venv/bin/activate

# Run the indexing script
python -m src.scripts.index_chapters
```

## Building for Production

### Frontend build
```bash
# From the frontend directory
cd frontend

# Build for GitHub Pages deployment
npm run build
```

### Backend deployment
```bash
# Ensure all environment variables are set appropriately for production
# The backend can be deployed as a standard FastAPI application
```

## Deployment to GitHub Pages

1. Build the frontend: `npm run build`
2. The static files will be in the `build` directory
3. Configure GitHub Pages to serve from the `build` directory

## Adding New Book Chapters

1. Create a new Markdown file in `docs/chapters/` following the naming convention
2. Add the chapter to the `sidebars.js` file in the frontend directory
3. Run the chapter indexing script to add it to the RAG system

## Troubleshooting

- If you encounter issues with Python dependencies, ensure you're using Python 3.11+
- For database connection issues, verify your `DATABASE_URL` is correctly configured
- If the RAG chatbot isn't working, check that your Qdrant and OpenAI API keys are valid
- For authentication issues, verify that Better-Auth is properly configured