# LeetCode Learning Tool

A comprehensive web application for learning and mastering LeetCode problems. Features detailed solutions, multiple approaches, complexity analysis, and key insights for common coding interview questions.

## Features

- Browse and search LeetCode problems
- Multiple solution approaches with detailed explanations
- Time and space complexity analysis
- Key insights and learning patterns
- Edge cases documentation
- Similar problems recommendations
- Clean, responsive UI built with React and Tailwind CSS
- Fast API backend with FastAPI

## Project Structure

```
leetcode-learning-tool/
├── backend/              # FastAPI backend
│   ├── api/             # API routes
│   ├── data/            # Solutions database (JSON)
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   └── main.py          # FastAPI application entry point
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   ├── App.jsx      # Main application component
│   │   └── main.jsx     # React entry point
│   └── dist/           # Production build output
├── tests/              # Backend tests
└── docs/               # Additional documentation
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the project root:
```bash
cd leetcode-learning-tool
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r backend/requirements.txt
```

4. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env if needed (defaults work for local development)
```

5. Run the backend server:
```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation (Swagger UI): `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Production Build

To create a production build of the frontend:
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## Running Tests

Run the backend test suite:
```bash
python -m pytest tests/ -v
```

## API Endpoints

- `GET /api/problems` - Get all problems (with optional filters)
- `GET /api/problems/{problem_id}` - Get specific problem by ID
- `GET /api/problems/by-url?url={leetcode_url}` - Get problem by LeetCode URL
- `GET /api/search?q={query}` - Search problems by title or topic

See `backend/README.md` for detailed API documentation.

## Technology Stack

### Backend
- FastAPI - Modern Python web framework
- Pydantic - Data validation using Python type annotations
- Uvicorn - ASGI server
- pytest - Testing framework

### Frontend
- React 18 - UI library
- React Router - Client-side routing
- Axios - HTTP client
- Tailwind CSS - Utility-first CSS framework
- Vite - Build tool and dev server

## Current Problem Coverage

- Two Sum
- Valid Parentheses
- (More problems to be added)

## Development

### Adding New Solutions

Solutions are stored in `backend/data/solutions.json`. Each solution includes:
- Problem metadata (title, difficulty, topics, LeetCode URL)
- Multiple solution approaches with code
- Time and space complexity analysis
- Detailed explanations
- Key insights and learning patterns
- Edge cases
- Similar problems

See existing entries in `solutions.json` for the format.

### Code Style

- Backend: Follow PEP 8 Python style guide
- Frontend: Follow standard React/JavaScript conventions
- Use meaningful variable names and add comments for complex logic

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for educational purposes.

## Resources

- [LeetCode](https://leetcode.com/) - Practice problems
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Backend framework
- [React Documentation](https://react.dev/) - Frontend library
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
