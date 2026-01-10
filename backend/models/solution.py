from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Literal


class SolutionApproach(BaseModel):
    """A single approach to solving the problem."""
    approach: str
    time_complexity: str
    space_complexity: str
    code: str
    explanation: str


class SimilarProblem(BaseModel):
    """Reference to a similar problem."""
    title: str
    url: HttpUrl


class Solution(BaseModel):
    """Complete solution package for a LeetCode problem."""
    problem_id: str
    title: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    topics: List[str]
    leetcode_url: HttpUrl
    solutions: List[SolutionApproach]
    key_insights: List[str]
    edge_cases: List[str]
    similar_problems: List[SimilarProblem]
