#!/usr/bin/env python3
"""
Generate comprehensive LeetCode solutions using Claude Code.

Usage:
    python generate_solutions.py --test    # Generate 2 test problems
    python generate_solutions.py --full    # Generate all 30+ problems
"""

import json
import sys
from pathlib import Path
from backend.data.problem_list import TEST_PROBLEMS, FULL_PROBLEM_LIST


def generate_solution_for_problem(problem: dict) -> dict:
    """
    Generate a comprehensive solution for a single problem.

    This function is designed to be called interactively with Claude Code.
    When run, it will prompt you to provide the solution data.
    """
    print(f"\n{'='*60}")
    print(f"Generating solution for: {problem['title']}")
    print(f"Difficulty: {problem['difficulty']}")
    print(f"URL: {problem['leetcode_url']}")
    print(f"{'='*60}\n")

    print("Please provide the following information for this problem:")
    print("1. Topics (comma-separated, e.g., 'Array,Hash Table')")
    print("2. Number of solution approaches")
    print("For each approach:")
    print("   - Approach name")
    print("   - Time complexity")
    print("   - Space complexity")
    print("   - Python code")
    print("   - Detailed explanation")
    print("3. Key insights (one per line)")
    print("4. Edge cases (one per line)")
    print("5. Similar problems (title and URL)")

    # This is where Claude Code will help generate the actual solution
    # For now, return a placeholder structure
    return {
        "problem_id": problem["problem_id"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "topics": [],
        "leetcode_url": problem["leetcode_url"],
        "solutions": [],
        "key_insights": [],
        "edge_cases": [],
        "similar_problems": []
    }


def save_solutions(solutions: list[dict], output_file: Path):
    """Save generated solutions to JSON file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(solutions, f, indent=2)
    print(f"\nSolutions saved to: {output_file}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ['--test', '--full']:
        print("Usage: python generate_solutions.py [--test|--full]")
        sys.exit(1)

    mode = sys.argv[1]
    problems = TEST_PROBLEMS if mode == '--test' else FULL_PROBLEM_LIST

    print(f"Generating solutions for {len(problems)} problems...")
    print("This process requires Claude Code interaction for each problem.\n")

    solutions = []
    for problem in problems:
        solution = generate_solution_for_problem(problem)
        solutions.append(solution)

    output_file = Path("backend/data/solutions.json")
    save_solutions(solutions, output_file)

    print(f"\nSuccessfully generated {len(solutions)} solutions")


if __name__ == "__main__":
    main()
