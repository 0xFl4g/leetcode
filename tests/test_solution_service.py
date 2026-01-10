import pytest
import json
from pathlib import Path
from backend.services.solution_service import SolutionService
from backend.models.solution import Solution


@pytest.fixture
def sample_solutions_file(tmp_path):
    """Create a temporary solutions file for testing."""
    solutions = [
        {
            "problem_id": "two-sum",
            "title": "Two Sum",
            "difficulty": "Easy",
            "topics": ["Array", "Hash Table"],
            "leetcode_url": "https://leetcode.com/problems/two-sum/",
            "solutions": [],
            "key_insights": [],
            "edge_cases": [],
            "similar_problems": []
        },
        {
            "problem_id": "valid-parentheses",
            "title": "Valid Parentheses",
            "difficulty": "Easy",
            "topics": ["String", "Stack"],
            "leetcode_url": "https://leetcode.com/problems/valid-parentheses/",
            "solutions": [],
            "key_insights": [],
            "edge_cases": [],
            "similar_problems": []
        }
    ]

    file_path = tmp_path / "solutions.json"
    with open(file_path, 'w') as f:
        json.dump(solutions, f)

    return file_path


def test_solution_service_loads_data(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    assert len(service.solutions) == 2


def test_get_all_problems(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    problems = service.get_all_problems()
    assert len(problems) == 2
    assert problems[0]["title"] == "Two Sum"


def test_get_problem_by_id(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    problem = service.get_problem_by_id("two-sum")
    assert problem is not None
    assert problem.title == "Two Sum"


def test_get_problem_by_id_not_found(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    problem = service.get_problem_by_id("nonexistent")
    assert problem is None


def test_filter_by_difficulty(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    problems = service.get_all_problems(difficulty="Easy")
    assert len(problems) == 2


def test_filter_by_topic(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    problems = service.get_all_problems(topic="Array")
    assert len(problems) == 1
    assert problems[0]["problem_id"] == "two-sum"


def test_search_problems(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    results = service.search_problems("sum")
    assert len(results) == 1
    assert results[0]["title"] == "Two Sum"


def test_get_problem_by_url(sample_solutions_file):
    service = SolutionService(str(sample_solutions_file))
    problem = service.get_problem_by_url("https://leetcode.com/problems/two-sum/")
    assert problem is not None
    assert problem.problem_id == "two-sum"
