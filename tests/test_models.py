import pytest
from backend.models.solution import Solution, SolutionApproach


def test_solution_approach_creation():
    approach = SolutionApproach(
        approach="Brute Force",
        time_complexity="O(n²)",
        space_complexity="O(1)",
        code="def solution(): pass",
        explanation="Simple brute force approach"
    )
    assert approach.approach == "Brute Force"
    assert approach.time_complexity == "O(n²)"


def test_solution_creation():
    solution = Solution(
        problem_id="two-sum",
        title="Two Sum",
        difficulty="Easy",
        topics=["Array", "Hash Table"],
        leetcode_url="https://leetcode.com/problems/two-sum/",
        solutions=[],
        key_insights=["Use hash map"],
        edge_cases=["Empty array"],
        similar_problems=[]
    )
    assert solution.problem_id == "two-sum"
    assert solution.difficulty == "Easy"
    assert len(solution.topics) == 2


def test_solution_with_multiple_approaches():
    approach1 = SolutionApproach(
        approach="Brute Force",
        time_complexity="O(n²)",
        space_complexity="O(1)",
        code="def solution(): pass",
        explanation="Brute force"
    )
    approach2 = SolutionApproach(
        approach="Hash Map",
        time_complexity="O(n)",
        space_complexity="O(n)",
        code="def solution(): pass",
        explanation="Optimal"
    )
    solution = Solution(
        problem_id="two-sum",
        title="Two Sum",
        difficulty="Easy",
        topics=["Array"],
        leetcode_url="https://leetcode.com/problems/two-sum/",
        solutions=[approach1, approach2],
        key_insights=[],
        edge_cases=[],
        similar_problems=[]
    )
    assert len(solution.solutions) == 2
