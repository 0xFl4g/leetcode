# LeetCode Solutions

> **Educational Resource**: A collection of LeetCode problem solutions for learning algorithmic problem-solving patterns and techniques.

A web application for browsing and studying LeetCode solutions. Features a modern dark-themed UI, full-text search with BM25 ranking, and detailed complexity analysis.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![React](https://img.shields.io/badge/React-19-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Full-text search** with BM25 ranking and result highlighting
- **Multiple solution approaches** with detailed explanations
- **Complexity analysis** for time and space
- **Dark mode UI** with Gmail-style master-detail layout
- **Filter by difficulty** (Easy, Medium, Hard)
- **Search by topic** (Array, Hash Table, Stack, etc.)
- **Fast SQLite backend** with FTS5 full-text search

## Screenshots

The interface features a split-panel layout:
- Left panel: Searchable problem list with difficulty badges
- Right panel: Solution details with syntax-highlighted code

## Quick Start

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Bun](https://bun.sh) (JavaScript runtime)

### Backend

```bash
# Install dependencies
uv sync

# Run the server
uv run uvicorn backend.main:app --reload --port 8001
```

API available at `http://localhost:8001` | Docs at `http://localhost:8001/docs`

### Frontend

```bash
cd frontend

# Install dependencies
bun install

# Start dev server
bun run dev
```

Frontend available at `http://localhost:5173`

### Production Build

```bash
cd frontend
bun run build
```

## Project Structure

```
├── backend/
│   ├── api/              # FastAPI routes
│   ├── db/               # SQLite database & migrations
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   └── main.py           # Application entry
├── frontend/
│   └── src/
│       ├── components/   # React components
│       ├── hooks/        # Custom React hooks
│       ├── services/     # API client
│       ├── types/        # TypeScript definitions
│       └── App.tsx       # Main application
└── tests/                # pytest test suite
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/problems` | List problems (supports `difficulty`, `topic`, `limit`, `offset`) |
| `GET /api/problems/{id}` | Get problem details with solutions |
| `GET /api/search?q={query}` | Full-text search with highlighting |
| `GET /api/stats` | Problem statistics by difficulty |

## Tech Stack

**Backend:** FastAPI, SQLite with FTS5, Pydantic, pytest

**Frontend:** React 19, TypeScript, Tailwind CSS 4, Vite, React Router

## Running Tests

```bash
uv run pytest tests/ -v
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Resources

- [LeetCode](https://leetcode.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
