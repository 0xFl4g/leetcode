import pytest
import sqlite3
from pathlib import Path
from backend.services.solution_service import SolutionService


@pytest.fixture
def test_db(tmp_path):
    """Create a temporary SQLite database for testing."""
    db_path = tmp_path / "test_solutions.db"
    conn = sqlite3.connect(db_path)

    # Create schema
    conn.executescript("""
        CREATE TABLE problems (
            problem_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            leetcode_url TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE solutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id TEXT NOT NULL REFERENCES problems(problem_id),
            approach_name TEXT NOT NULL,
            time_complexity TEXT,
            space_complexity TEXT,
            code TEXT NOT NULL,
            source_hash TEXT NOT NULL,
            UNIQUE(problem_id, approach_name)
        );

        CREATE TABLE enrichments (
            problem_id TEXT PRIMARY KEY REFERENCES problems(problem_id),
            difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
            topics TEXT DEFAULT '[]',
            explanation TEXT DEFAULT '',
            key_insights TEXT DEFAULT '[]',
            edge_cases TEXT DEFAULT '[]',
            similar_problems TEXT DEFAULT '[]',
            needs_review INTEGER DEFAULT 0,
            reviewed_at TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE source_metadata (
            problem_id TEXT PRIMARY KEY REFERENCES problems(problem_id),
            file_hash TEXT NOT NULL,
            fetched_at TEXT DEFAULT (datetime('now')),
            source_url TEXT NOT NULL
        );

        CREATE VIRTUAL TABLE problems_fts USING fts5(
            problem_id UNINDEXED,
            title,
            topics,
            approaches,
            tokenize='porter unicode61 remove_diacritics 1'
        );
    """)

    # Insert test data
    conn.execute("""
        INSERT INTO problems (problem_id, title, leetcode_url)
        VALUES ('two-sum', 'Two Sum', 'https://leetcode.com/problems/two-sum/')
    """)
    conn.execute("""
        INSERT INTO problems (problem_id, title, leetcode_url)
        VALUES ('valid-parentheses', 'Valid Parentheses', 'https://leetcode.com/problems/valid-parentheses/')
    """)

    conn.execute("""
        INSERT INTO solutions (problem_id, approach_name, time_complexity, space_complexity, code, source_hash)
        VALUES ('two-sum', 'Optimal Solution', 'O(n)', 'O(n)', 'class Solution: pass', 'abc123')
    """)
    conn.execute("""
        INSERT INTO solutions (problem_id, approach_name, time_complexity, space_complexity, code, source_hash)
        VALUES ('valid-parentheses', 'Optimal Solution', 'O(n)', 'O(n)', 'class Solution: pass', 'def456')
    """)

    conn.execute("""
        INSERT INTO enrichments (problem_id, difficulty, topics)
        VALUES ('two-sum', 'Easy', '["Array", "Hash Table"]')
    """)
    conn.execute("""
        INSERT INTO enrichments (problem_id, difficulty, topics)
        VALUES ('valid-parentheses', 'Easy', '["String", "Stack"]')
    """)

    conn.execute("""
        INSERT INTO source_metadata (problem_id, file_hash, source_url)
        VALUES ('two-sum', 'hash1', 'path/two-sum.py')
    """)
    conn.execute("""
        INSERT INTO source_metadata (problem_id, file_hash, source_url)
        VALUES ('valid-parentheses', 'hash2', 'path/valid-parentheses.py')
    """)

    # Populate FTS with all searchable columns
    conn.execute("""
        INSERT INTO problems_fts (problem_id, title, topics, approaches)
        SELECT
            p.problem_id,
            p.title,
            COALESCE(REPLACE(REPLACE(REPLACE(e.topics, '[', ''), ']', ''), '"', ''), ''),
            COALESCE(GROUP_CONCAT(s.approach_name, ' '), '')
        FROM problems p
        LEFT JOIN enrichments e ON p.problem_id = e.problem_id
        LEFT JOIN solutions s ON p.problem_id = s.problem_id
        GROUP BY p.problem_id
    """)

    conn.commit()
    conn.close()

    return db_path


def test_get_all_problems(test_db):
    service = SolutionService(str(test_db))
    problems = service.get_all_problems()
    assert len(problems) == 2


def test_get_problem_by_id(test_db):
    service = SolutionService(str(test_db))
    problem = service.get_problem_by_id("two-sum")
    assert problem is not None
    assert problem.title == "Two Sum"
    assert problem.difficulty == "Easy"
    assert len(problem.solutions) == 1


def test_get_problem_by_id_not_found(test_db):
    service = SolutionService(str(test_db))
    problem = service.get_problem_by_id("nonexistent")
    assert problem is None


def test_filter_by_difficulty(test_db):
    service = SolutionService(str(test_db))
    problems = service.get_all_problems(difficulty="Easy")
    assert len(problems) == 2


def test_filter_by_topic(test_db):
    service = SolutionService(str(test_db))
    problems = service.get_all_problems(topic="Array")
    assert len(problems) == 1
    assert problems[0]["problem_id"] == "two-sum"


def test_search_problems(test_db):
    service = SolutionService(str(test_db))
    results = service.search_problems("sum")
    assert len(results) >= 1
    assert any(r["title"] == "Two Sum" for r in results)


def test_get_problem_by_url(test_db):
    service = SolutionService(str(test_db))
    problem = service.get_problem_by_url("https://leetcode.com/problems/two-sum/")
    assert problem is not None
    assert problem.problem_id == "two-sum"


def test_get_stats(test_db):
    service = SolutionService(str(test_db))
    stats = service.get_stats()
    assert stats["total_problems"] == 2
    assert stats["total_solutions"] == 2
    assert stats["by_difficulty"]["Easy"] == 2


def test_update_enrichment(test_db):
    service = SolutionService(str(test_db))
    success = service.update_enrichment(
        "two-sum",
        topics=["Array", "Hash Table", "Two Pointers"],
        explanation="Use a hash map for O(n) lookup."
    )
    assert success

    problem = service.get_problem_by_id("two-sum")
    assert "Two Pointers" in problem.topics


def test_pagination(test_db):
    service = SolutionService(str(test_db))
    # Get first problem only
    problems = service.get_all_problems(limit=1, offset=0)
    assert len(problems) == 1

    # Get second problem
    problems_offset = service.get_all_problems(limit=1, offset=1)
    assert len(problems_offset) == 1
    assert problems[0]["problem_id"] != problems_offset[0]["problem_id"]


def test_search_returns_highlights(test_db):
    service = SolutionService(str(test_db))
    results = service.search_problems("sum")
    assert len(results) >= 1
    # Verify highlight fields are present
    result = next(r for r in results if r["title"] == "Two Sum")
    assert "highlight" in result
    assert result["highlight"] is not None
    assert "title" in result["highlight"]


def test_search_empty_query(test_db):
    service = SolutionService(str(test_db))
    results = service.search_problems("")
    assert results == []


def test_search_special_characters(test_db):
    service = SolutionService(str(test_db))
    # Should not crash with special FTS characters
    results = service.search_problems("sum OR parentheses")
    assert isinstance(results, list)

    # Quotes should be handled
    results = service.search_problems('"two sum"')
    assert isinstance(results, list)


def test_search_by_topic(test_db):
    service = SolutionService(str(test_db))
    # Search for a topic that exists in the FTS index
    results = service.search_problems("Array")
    assert len(results) >= 1


def test_get_problem_by_url_not_found(test_db):
    service = SolutionService(str(test_db))
    problem = service.get_problem_by_url("https://leetcode.com/problems/nonexistent/")
    assert problem is None


def test_get_problems_needing_review(test_db):
    service = SolutionService(str(test_db))
    # Initially no problems need review (needs_review=0 by default)
    problems = service.get_problems_needing_review()
    assert isinstance(problems, list)


def test_mark_reviewed(test_db):
    service = SolutionService(str(test_db))
    # Mark a problem as reviewed
    success = service.mark_reviewed("two-sum")
    assert success

    # Mark nonexistent problem
    success = service.mark_reviewed("nonexistent")
    assert not success
