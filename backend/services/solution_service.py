import json
from pathlib import Path
from typing import List, Optional
from backend.models.solution import Solution


class SolutionService:
    """Service for loading and querying LeetCode solutions."""

    def __init__(self, solutions_file: str = "backend/data/solutions.json"):
        self.solutions_file = Path(solutions_file)
        self.solutions: List[Solution] = []
        self._load_solutions()

    def _load_solutions(self):
        """Load solutions from JSON file into memory."""
        if not self.solutions_file.exists():
            raise FileNotFoundError(f"Solutions file not found: {self.solutions_file}")

        with open(self.solutions_file, 'r') as f:
            data = json.load(f)
            self.solutions = [Solution(**item) for item in data]

    def get_all_problems(
        self,
        difficulty: Optional[str] = None,
        topic: Optional[str] = None
    ) -> List[dict]:
        """
        Get list of all problems with basic info.

        Args:
            difficulty: Filter by difficulty (Easy, Medium, Hard)
            topic: Filter by topic (e.g., "Array", "Hash Table")

        Returns:
            List of problem summaries
        """
        filtered = self.solutions

        if difficulty:
            filtered = [s for s in filtered if s.difficulty == difficulty]

        if topic:
            filtered = [s for s in filtered if topic in s.topics]

        return [
            {
                "problem_id": s.problem_id,
                "title": s.title,
                "difficulty": s.difficulty,
                "topics": s.topics,
                "leetcode_url": s.leetcode_url
            }
            for s in filtered
        ]

    def get_problem_by_id(self, problem_id: str) -> Optional[Solution]:
        """Get full solution by problem ID."""
        for solution in self.solutions:
            if solution.problem_id == problem_id:
                return solution
        return None

    def search_problems(self, query: str) -> List[dict]:
        """
        Search problems by title or topics.

        Args:
            query: Search string (case-insensitive)

        Returns:
            List of matching problem summaries
        """
        query_lower = query.lower()
        results = []

        for solution in self.solutions:
            # Search in title
            if query_lower in solution.title.lower():
                results.append({
                    "problem_id": solution.problem_id,
                    "title": solution.title,
                    "difficulty": solution.difficulty,
                    "topics": solution.topics,
                    "leetcode_url": solution.leetcode_url
                })
                continue

            # Search in topics
            for topic in solution.topics:
                if query_lower in topic.lower():
                    results.append({
                        "problem_id": solution.problem_id,
                        "title": solution.title,
                        "difficulty": solution.difficulty,
                        "topics": solution.topics,
                        "leetcode_url": solution.leetcode_url
                    })
                    break

        return results

    def get_problem_by_url(self, url: str) -> Optional[Solution]:
        """Get full solution by LeetCode URL."""
        for solution in self.solutions:
            if str(solution.leetcode_url) == url:
                return solution
        return None
