import json
import sqlite3
from pathlib import Path
from typing import Optional

from backend.models.solution import Solution, SolutionApproach, SimilarProblem


class SolutionService:
    """Service for loading and querying LeetCode solutions from SQLite."""

    def __init__(self, db_path: str = "backend/db/solutions.db"):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all_problems(
        self,
        difficulty: Optional[str] = None,
        topic: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[dict]:
        """
        Get list of all problems with basic info.

        Args:
            difficulty: Filter by difficulty (Easy, Medium, Hard)
            topic: Filter by topic (e.g., "Array", "Hash Table")
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of problem summaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = """
            SELECT p.problem_id, p.title, p.leetcode_url,
                   e.difficulty,
                   COALESCE(e.topics, '[]') as topics
            FROM problems p
            LEFT JOIN enrichments e ON p.problem_id = e.problem_id
            WHERE 1=1
        """
        params: list = []

        if difficulty:
            query += " AND e.difficulty = ?"
            params.append(difficulty)

        if topic:
            # Search in JSON array
            query += " AND e.topics LIKE ?"
            params.append(f'%"{topic}"%')

        query += " ORDER BY p.title LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)

        results = []
        for row in cursor.fetchall():
            results.append({
                "problem_id": row["problem_id"],
                "title": row["title"],
                "difficulty": row["difficulty"],  # Can be None
                "topics": json.loads(row["topics"]),
                "leetcode_url": row["leetcode_url"]
            })

        conn.close()
        return results

    def get_problem_by_id(self, problem_id: str) -> Optional[Solution]:
        """Get full solution by problem ID."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get problem info
        cursor.execute("""
            SELECT p.problem_id, p.title, p.leetcode_url,
                   e.difficulty,
                   COALESCE(e.topics, '[]') as topics,
                   COALESCE(e.explanation, '') as explanation,
                   COALESCE(e.key_insights, '[]') as key_insights,
                   COALESCE(e.edge_cases, '[]') as edge_cases,
                   COALESCE(e.similar_problems, '[]') as similar_problems,
                   COALESCE(e.needs_review, 0) as needs_review
            FROM problems p
            LEFT JOIN enrichments e ON p.problem_id = e.problem_id
            WHERE p.problem_id = ?
        """, (problem_id,))

        problem_row = cursor.fetchone()
        if not problem_row:
            conn.close()
            return None

        # Get all solution approaches
        cursor.execute("""
            SELECT approach_name, time_complexity, space_complexity, code
            FROM solutions
            WHERE problem_id = ?
            ORDER BY id
        """, (problem_id,))

        solutions = []
        for sol_row in cursor.fetchall():
            solutions.append(SolutionApproach(
                approach=sol_row["approach_name"],
                time_complexity=sol_row["time_complexity"] or "Unknown",
                space_complexity=sol_row["space_complexity"] or "Unknown",
                code=sol_row["code"],
                explanation=""  # Per-approach explanations could be added later
            ))

        # Parse JSON fields
        similar_problems = []
        for sp in json.loads(problem_row["similar_problems"]):
            if isinstance(sp, dict) and "title" in sp and "url" in sp:
                similar_problems.append(SimilarProblem(title=sp["title"], url=sp["url"]))

        conn.close()

        return Solution(
            problem_id=problem_row["problem_id"],
            title=problem_row["title"],
            difficulty=problem_row["difficulty"],
            topics=json.loads(problem_row["topics"]),
            leetcode_url=problem_row["leetcode_url"],
            solutions=solutions,
            key_insights=json.loads(problem_row["key_insights"]),
            edge_cases=json.loads(problem_row["edge_cases"]),
            similar_problems=similar_problems
        )

    def search_problems(self, query: str, limit: int = 50) -> list[dict]:
        """
        Search problems using enhanced full-text search with BM25 ranking.

        Searches across:
        - Problem titles (highest weight)
        - Topics
        - Solution approach names

        Args:
            query: Search string (supports phrases with quotes)
            limit: Maximum number of results

        Returns:
            List of matching problem summaries with relevance scores and highlights
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Clean and prepare query for FTS5
        # Handle quoted phrases and add prefix matching for partial words
        search_query = self._prepare_fts_query(query)

        if not search_query:
            conn.close()
            return []

        # Use BM25 ranking with column weights: title(10), topics(5), approaches(3)
        # highlight() returns the matched text with markers
        cursor.execute("""
            SELECT
                fts.problem_id,
                p.title,
                p.leetcode_url,
                e.difficulty,
                COALESCE(e.topics, '[]') as topics,
                bm25(problems_fts, 10.0, 5.0, 3.0) as rank,
                highlight(problems_fts, 1, '<mark>', '</mark>') as title_highlight,
                snippet(problems_fts, 2, '<mark>', '</mark>', '...', 10) as topics_snippet
            FROM problems_fts fts
            JOIN problems p ON fts.problem_id = p.problem_id
            LEFT JOIN enrichments e ON p.problem_id = e.problem_id
            WHERE problems_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (search_query, limit))

        results = []
        for row in cursor.fetchall():
            results.append({
                "problem_id": row["problem_id"],
                "title": row["title"],
                "difficulty": row["difficulty"],
                "topics": json.loads(row["topics"]),
                "leetcode_url": row["leetcode_url"],
                "score": abs(row["rank"]),  # BM25 returns negative scores
                "highlight": {
                    "title": row["title_highlight"],
                    "topics": row["topics_snippet"] if row["topics_snippet"] else None
                }
            })

        # If FTS found nothing, fall back to LIKE search
        if not results:
            cursor.execute("""
                SELECT p.problem_id, p.title, p.leetcode_url,
                       e.difficulty,
                       COALESCE(e.topics, '[]') as topics
                FROM problems p
                LEFT JOIN enrichments e ON p.problem_id = e.problem_id
                WHERE p.title LIKE ?
                   OR e.topics LIKE ?
                ORDER BY p.title
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))

            for row in cursor.fetchall():
                results.append({
                    "problem_id": row["problem_id"],
                    "title": row["title"],
                    "difficulty": row["difficulty"],
                    "topics": json.loads(row["topics"]),
                    "leetcode_url": row["leetcode_url"],
                    "score": 0,
                    "highlight": None
                })

        conn.close()
        return results

    def _prepare_fts_query(self, query: str) -> str:
        """
        Prepare a search query for FTS5.

        Handles:
        - Quoted phrases: "two sum" -> "two sum"
        - Multiple words: two sum -> two* sum*
        - Special characters removal

        Args:
            query: Raw user query

        Returns:
            FTS5-compatible query string
        """
        import re

        query = query.strip()
        if not query:
            return ""

        # If query is quoted, treat as phrase search
        if query.startswith('"') and query.endswith('"'):
            return query

        # Remove special FTS5 characters that could cause syntax errors
        query = re.sub(r'[^\w\s"-]', ' ', query)

        # Split into words and add prefix matching
        words = query.split()
        if not words:
            return ""

        # FTS5 operators that should not have * appended
        fts_operators = {"OR", "AND", "NOT"}

        # For single word, use prefix match
        if len(words) == 1:
            word = words[0]
            return word if word.upper() in fts_operators else f"{word}*"

        # For multiple words, use prefix match on each (except operators)
        # This allows "two su" to match "two sum"
        processed = []
        for word in words:
            if word.upper() in fts_operators:
                processed.append(word.upper())  # Normalize operators to uppercase
            else:
                processed.append(f"{word}*")
        return " ".join(processed)

    def get_problem_by_url(self, url: str) -> Optional[Solution]:
        """Get full solution by LeetCode URL."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT problem_id FROM problems WHERE leetcode_url = ?",
            (url,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return self.get_problem_by_id(row["problem_id"])
        return None

    def get_stats(self) -> dict:
        """Get database statistics."""
        conn = self._get_connection()
        cursor = conn.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) FROM problems")
        stats["total_problems"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM solutions")
        stats["total_solutions"] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT difficulty, COUNT(*) as count
            FROM enrichments
            WHERE difficulty IS NOT NULL
            GROUP BY difficulty
        """)
        stats["by_difficulty"] = {
            row["difficulty"]: row["count"]
            for row in cursor.fetchall()
        }

        cursor.execute("SELECT COUNT(*) FROM enrichments WHERE needs_review = 1")
        stats["needs_review"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM enrichments WHERE explanation != ''")
        stats["with_explanations"] = cursor.fetchone()[0]

        conn.close()
        return stats

    def get_problems_needing_review(self, limit: int = 50) -> list[dict]:
        """Get problems where source has changed since last review."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.problem_id, p.title, p.leetcode_url,
                   e.difficulty,
                   COALESCE(e.topics, '[]') as topics
            FROM problems p
            JOIN enrichments e ON p.problem_id = e.problem_id
            WHERE e.needs_review = 1
            LIMIT ?
        """, (limit,))

        results = []
        for row in cursor.fetchall():
            results.append({
                "problem_id": row["problem_id"],
                "title": row["title"],
                "difficulty": row["difficulty"],
                "topics": json.loads(row["topics"]),
                "leetcode_url": row["leetcode_url"]
            })

        conn.close()
        return results

    def mark_reviewed(self, problem_id: str) -> bool:
        """Mark a problem as reviewed (clears needs_review flag)."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE enrichments
            SET needs_review = 0, reviewed_at = datetime('now')
            WHERE problem_id = ?
        """, (problem_id,))

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0

    def update_enrichment(
        self,
        problem_id: str,
        topics: Optional[list[str]] = None,
        explanation: Optional[str] = None,
        key_insights: Optional[list[str]] = None,
        edge_cases: Optional[list[str]] = None,
        similar_problems: Optional[list[dict]] = None
    ) -> bool:
        """Update enrichment data for a problem."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Build update query dynamically
        updates = []
        params = []

        if topics is not None:
            updates.append("topics = ?")
            params.append(json.dumps(topics))

        if explanation is not None:
            updates.append("explanation = ?")
            params.append(explanation)

        if key_insights is not None:
            updates.append("key_insights = ?")
            params.append(json.dumps(key_insights))

        if edge_cases is not None:
            updates.append("edge_cases = ?")
            params.append(json.dumps(edge_cases))

        if similar_problems is not None:
            updates.append("similar_problems = ?")
            params.append(json.dumps(similar_problems))

        if not updates:
            return False

        updates.append("updated_at = datetime('now')")
        params.append(problem_id)

        query = f"UPDATE enrichments SET {', '.join(updates)} WHERE problem_id = ?"
        cursor.execute(query, params)

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0
