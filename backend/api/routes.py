from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.services.solution_service import SolutionService
from backend.models.solution import Solution

router = APIRouter()

# Initialize service (loads solutions into memory)
solution_service = SolutionService()


@router.get("/problems")
def get_all_problems(
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    topic: Optional[str] = Query(None, description="Filter by topic")
):
    """Get list of all problems with optional filtering."""
    return solution_service.get_all_problems(difficulty=difficulty, topic=topic)


@router.get("/search")
def search_problems(q: str = Query(..., description="Search query")):
    """Search problems by title or topics."""
    return solution_service.search_problems(q)


@router.get("/problems/by-url", response_model=Solution)
def get_problem_by_url(url: str = Query(..., description="LeetCode problem URL")):
    """Get full solution by LeetCode URL."""
    solution = solution_service.get_problem_by_url(url)
    if solution is None:
        raise HTTPException(
            status_code=404,
            detail=f"Problem with URL '{url}' not found"
        )
    return solution


@router.get("/problems/{problem_id}", response_model=Solution)
def get_problem_by_id(problem_id: str):
    """Get full solution for a specific problem."""
    solution = solution_service.get_problem_by_id(problem_id)
    if solution is None:
        raise HTTPException(
            status_code=404,
            detail=f"Problem '{problem_id}' not found"
        )
    return solution
