from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.services.solution_service import SolutionService
from backend.models.solution import Solution

router = APIRouter()

# Initialize service
solution_service = SolutionService()


@router.get("/stats")
def get_stats():
    """Get database statistics."""
    return solution_service.get_stats()


@router.get("/problems")
def get_all_problems(
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    limit: int = Query(100, ge=1, le=1000, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """Get list of all problems with optional filtering and pagination."""
    return solution_service.get_all_problems(
        difficulty=difficulty, topic=topic, limit=limit, offset=offset
    )


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


@router.get("/problems/needs-review")
def get_problems_needing_review(
    limit: int = Query(50, ge=1, le=200, description="Max results")
):
    """Get problems where upstream source has changed since last review."""
    return solution_service.get_problems_needing_review(limit=limit)


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


@router.post("/problems/{problem_id}/mark-reviewed")
def mark_problem_reviewed(problem_id: str):
    """Mark a problem as reviewed (clears needs_review flag)."""
    success = solution_service.mark_reviewed(problem_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Problem '{problem_id}' not found"
        )
    return {"status": "ok", "problem_id": problem_id}
