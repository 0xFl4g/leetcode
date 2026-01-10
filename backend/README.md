# LeetCode Learning Tool - Backend

FastAPI-based REST API for serving LeetCode problem solutions and metadata.

## Architecture

The backend follows a clean architecture pattern:

```
backend/
├── api/              # API layer (routes, endpoints)
│   └── routes.py     # Problem and solution endpoints
├── data/             # Data layer
│   └── solutions.json # Solution database
├── models/           # Domain models (Pydantic schemas)
│   └── solution.py   # Solution data models
├── services/         # Business logic layer
│   └── solution_service.py  # Solution retrieval and filtering
└── main.py          # Application entry point and configuration
```

## Setup

### Requirements

- Python 3.8 or higher
- pip package manager

### Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Configure environment (optional):
```bash
# Create .env file in project root
cp .env.example .env
```

Default configuration:
- CORS Origins: `http://localhost:5173` (frontend dev server)
- Log Level: `INFO`

### Running the Server

Development mode (with auto-reload):
```bash
uvicorn backend.main:app --reload --port 8000
```

Production mode:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive API Docs

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### Root Endpoint
```
GET /
```
Returns API status message.

**Response:**
```json
{
  "message": "LeetCode Learning Tool API"
}
```

#### Get All Problems
```
GET /api/problems
```
Returns a list of all problems with optional filtering.

**Query Parameters:**
- `difficulty` (optional): Filter by difficulty ("Easy", "Medium", "Hard")
- `topic` (optional): Filter by topic (e.g., "Array", "Hash Table", "Stack")

**Response:**
```json
[
  {
    "problem_id": "two-sum",
    "title": "Two Sum",
    "difficulty": "Easy",
    "topics": ["Array", "Hash Table"],
    "leetcode_url": "https://leetcode.com/problems/two-sum/"
  }
]
```

#### Get Problem by ID
```
GET /api/problems/{problem_id}
```
Returns full solution details for a specific problem.

**Path Parameters:**
- `problem_id`: Problem identifier (e.g., "two-sum")

**Response:** Full Solution object (see Data Models section)

#### Get Problem by URL
```
GET /api/problems/by-url?url={leetcode_url}
```
Returns full solution by LeetCode URL.

**Query Parameters:**
- `url`: Full LeetCode problem URL

**Response:** Full Solution object (see Data Models section)

#### Search Problems
```
GET /api/search?q={query}
```
Search problems by title or topics.

**Query Parameters:**
- `q`: Search query string

**Response:** List of matching problems

## Data Models

### Solution Model

```python
{
  "problem_id": str,           # Unique identifier
  "title": str,                # Problem title
  "difficulty": str,           # Easy | Medium | Hard
  "topics": List[str],         # Related topics/tags
  "leetcode_url": str,         # Official LeetCode URL
  "solutions": [               # Multiple solution approaches
    {
      "approach": str,         # Approach name
      "time_complexity": str,  # Big O notation
      "space_complexity": str, # Big O notation
      "code": str,            # Python implementation
      "explanation": str      # Detailed explanation
    }
  ],
  "key_insights": List[str],   # Learning points
  "edge_cases": List[str],     # Important edge cases
  "similar_problems": [        # Related problems
    {
      "title": str,
      "url": str
    }
  ]
}
```

## Adding New Solutions

Solutions are stored in `backend/data/solutions.json`. To add a new solution:

1. Follow the JSON structure shown in the Data Models section
2. Include at least one solution approach
3. Add time and space complexity analysis
4. Provide clear explanations
5. Document key insights and edge cases
6. Link to similar problems
7. Validate JSON syntax

Example:
```json
{
  "problem_id": "valid-parentheses",
  "title": "Valid Parentheses",
  "difficulty": "Easy",
  "topics": ["String", "Stack"],
  "leetcode_url": "https://leetcode.com/problems/valid-parentheses/",
  "solutions": [
    {
      "approach": "Stack",
      "time_complexity": "O(n)",
      "space_complexity": "O(n)",
      "code": "def isValid(s: str) -> bool:\n    ...",
      "explanation": "..."
    }
  ],
  "key_insights": ["..."],
  "edge_cases": ["..."],
  "similar_problems": [{"title": "...", "url": "..."}]
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `404` - Problem not found
- `422` - Invalid request parameters
- `500` - Internal server error

Error response format:
```json
{
  "detail": "Error message"
}
```

## Testing

Run the test suite:
```bash
# From project root
python -m pytest tests/ -v
```

Run with coverage:
```bash
python -m pytest tests/ --cov=backend --cov-report=html
```

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework
- **httpx**: Async HTTP client for testing

## CORS Configuration

CORS is configured to allow requests from the frontend during development.

Default allowed origins:
- `http://localhost:5173` (Vite dev server)

To configure custom origins, set the `CORS_ORIGINS` environment variable:
```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Logging

Logging is configured at application startup:
- Default level: INFO
- Logs unhandled exceptions
- Logs API requests (via Uvicorn)

Configure log level via environment variable:
```bash
LOG_LEVEL=DEBUG
```

## Performance Considerations

- Solutions are loaded into memory at startup for fast access
- No database required - JSON file serves as the data source
- In-memory filtering and search operations
- Suitable for small to medium solution databases
- For large datasets, consider migrating to a database (PostgreSQL, MongoDB)

## Future Enhancements

- Add solution caching
- Implement rate limiting
- Add user authentication for personalized features
- Support for multiple programming languages
- Add submission tracking
- Implement difficulty progression recommendations
