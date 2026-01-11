#!/usr/bin/env python3
"""
Fetch ALL LeetCode solutions from kamyu104/LeetCode-Solutions repository.

This script:
1. Clones/pulls the repo locally for fast access
2. Reads Python solution files from local disk
3. Computes content hashes for change detection
4. Stores everything in SQLite database

Usage:
    uv run python fetch_all_solutions.py              # Full import
    uv run python fetch_all_solutions.py --update     # Only import changed/new
    uv run python fetch_all_solutions.py --check      # Check for upstream changes
    uv run python fetch_all_solutions.py --stats      # Show database stats
"""

import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


# Configuration
REPO_URL = "https://github.com/kamyu104/LeetCode-Solutions.git"
CACHE_DIR = Path(".cache/kamyu104-leetcode")
DB_PATH = Path("backend/db/solutions.db")
SCHEMA_PATH = Path("backend/db/schema.sql")


@dataclass
class SolutionFile:
    """Metadata about a solution file."""
    path: Path
    problem_id: str


@dataclass
class ParsedSolution:
    """A parsed solution approach from a file."""
    approach_name: str
    time_complexity: str
    space_complexity: str
    code: str
    code_hash: str


def sha256_hash(content: str) -> str:
    """Compute SHA256 hash of content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def init_database() -> sqlite3.Connection:
    """Initialize SQLite database with schema."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Read and execute schema
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())

    conn.commit()
    return conn


def sync_repo() -> bool:
    """Clone or pull the repository."""
    if CACHE_DIR.exists() and (CACHE_DIR / ".git").exists():
        print("Pulling latest changes...")
        result = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=CACHE_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Git pull failed: {result.stderr}")
            return False
        if "Already up to date" in result.stdout:
            print("Already up to date.")
        else:
            print(result.stdout.strip())
    else:
        print(f"Cloning repository to {CACHE_DIR}...")
        CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "clone", "--depth=1", REPO_URL, str(CACHE_DIR)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Git clone failed: {result.stderr}")
            return False
        print("Clone complete.")
    return True


def get_all_solution_files() -> list[SolutionFile]:
    """Get list of all Python solution files from local repo."""
    python_dir = CACHE_DIR / "Python"
    if not python_dir.exists():
        print(f"Python directory not found: {python_dir}")
        return []

    files = []
    for path in sorted(python_dir.glob("*.py")):
        problem_id = path.stem  # filename without .py
        files.append(SolutionFile(path=path, problem_id=problem_id))

    print(f"Found {len(files)} solution files")
    return files


def read_solution_content(solution_file: SolutionFile) -> str | None:
    """Read the content of a solution file from local disk."""
    try:
        return solution_file.path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {solution_file.path}: {e}")
        return None


def parse_complexity(content: str) -> tuple[str, str]:
    """Extract time and space complexity from file header."""
    time_match = re.search(r"#\s*Time:\s*(.+)", content)
    space_match = re.search(r"#\s*Space:\s*(.+)", content)

    time_complexity = time_match.group(1).strip() if time_match else "Unknown"
    space_complexity = space_match.group(1).strip() if space_match else "Unknown"

    return time_complexity, space_complexity


def extract_title_from_id(problem_id: str) -> str:
    """Convert problem ID to title (e.g., 'two-sum' -> 'Two Sum')."""
    return ' '.join(word.capitalize() for word in problem_id.split('-'))


def extract_solution_classes(content: str) -> list[tuple[str, str]]:
    """Extract individual Solution class definitions with their names."""
    # Find all class definitions
    pattern = re.compile(
        r"(class\s+(Solution\d*)\s*\([^)]*\):.*?)(?=\nclass\s+|\Z)",
        re.DOTALL
    )

    matches = pattern.findall(content)

    if matches:
        return [(match[1], match[0].strip()) for match in matches]

    # Fallback: try to get everything after header
    class_start = re.search(r"^class\s+", content, re.MULTILINE)
    if class_start:
        code = content[class_start.start():].strip()
        return [("Solution", code)]

    return []


def parse_solution_file(content: str, problem_id: str) -> list[ParsedSolution]:
    """Parse a solution file into structured solutions."""
    time_complexity, space_complexity = parse_complexity(content)
    solution_classes = extract_solution_classes(content)

    solutions = []
    name_counts: dict[str, int] = {}

    for class_name, class_code in solution_classes:
        # Create readable approach name
        if class_name == "Solution":
            base_name = "Optimal Solution"
        else:
            num = class_name.replace("Solution", "")
            base_name = f"Alternative Solution {num}" if num else "Optimal Solution"

        # Handle duplicate names by appending a counter
        if base_name in name_counts:
            name_counts[base_name] += 1
            approach_name = f"{base_name} (v{name_counts[base_name]})"
        else:
            name_counts[base_name] = 1
            approach_name = base_name

        solutions.append(ParsedSolution(
            approach_name=approach_name,
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            code=class_code,
            code_hash=sha256_hash(class_code)
        ))

    return solutions


def store_solution(
    conn: sqlite3.Connection,
    solution_file: SolutionFile,
    content: str,
    parsed_solutions: list[ParsedSolution]
) -> bool:
    """Store solution in database. Returns True if new/updated."""
    problem_id = solution_file.problem_id
    file_hash = sha256_hash(content)

    cursor = conn.cursor()

    # Check if we already have this exact version
    cursor.execute(
        "SELECT file_hash FROM source_metadata WHERE problem_id = ?",
        (problem_id,)
    )
    existing = cursor.fetchone()

    if existing and existing['file_hash'] == file_hash:
        return False  # No changes

    # Determine if this is an update (needs_review flag)
    is_update = existing is not None

    # Insert/update problem
    title = extract_title_from_id(problem_id)
    leetcode_url = f"https://leetcode.com/problems/{problem_id}/"

    cursor.execute("""
        INSERT INTO problems (problem_id, title, leetcode_url, updated_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(problem_id) DO UPDATE SET
            title = excluded.title,
            leetcode_url = excluded.leetcode_url,
            updated_at = datetime('now')
    """, (problem_id, title, leetcode_url))

    # Delete old solutions for this problem
    cursor.execute("DELETE FROM solutions WHERE problem_id = ?", (problem_id,))

    # Insert new solutions
    for ps in parsed_solutions:
        cursor.execute("""
            INSERT INTO solutions (problem_id, approach_name, time_complexity, space_complexity, code, source_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (problem_id, ps.approach_name, ps.time_complexity, ps.space_complexity, ps.code, ps.code_hash))

    # Update source metadata
    cursor.execute("""
        INSERT INTO source_metadata (problem_id, file_hash, source_url, fetched_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(problem_id) DO UPDATE SET
            file_hash = excluded.file_hash,
            source_url = excluded.source_url,
            fetched_at = datetime('now')
    """, (problem_id, file_hash, str(solution_file.path)))

    # Create/update enrichments entry
    if is_update:
        # Mark for review if content changed
        cursor.execute("""
            UPDATE enrichments SET needs_review = 1, updated_at = datetime('now')
            WHERE problem_id = ?
        """, (problem_id,))
    else:
        cursor.execute("""
            INSERT OR IGNORE INTO enrichments (problem_id)
            VALUES (?)
        """, (problem_id,))

    return True


def process_solution_file(solution_file: SolutionFile) -> tuple[SolutionFile, str | None, list[ParsedSolution]]:
    """Read and parse a single solution file from local disk."""
    content = read_solution_content(solution_file)

    if content:
        parsed = parse_solution_file(content, solution_file.problem_id)
        return (solution_file, content, parsed)

    return (solution_file, None, [])


def import_all_solutions(update_only: bool = False):
    """Import all solutions from kamyu104's repository."""
    # Sync repo first
    if not sync_repo():
        print("Failed to sync repository")
        return

    conn = init_database()

    # Get list of all solution files
    solution_files = get_all_solution_files()

    if not solution_files:
        print("No solution files found")
        return

    print(f"Processing {len(solution_files)} solutions...")

    # Process with progress tracking
    new_count = 0
    error_count = 0

    for i, solution_file in enumerate(solution_files, 1):
        if i % 100 == 0 or i == len(solution_files):
            print(f"Progress: {i}/{len(solution_files)} ({new_count} new, {error_count} errors)")

        solution_file, content, parsed = process_solution_file(solution_file)

        if content and parsed:
            try:
                is_new = store_solution(conn, solution_file, content, parsed)
                if is_new:
                    new_count += 1
                conn.commit()
            except Exception as e:
                print(f"Error storing {solution_file.problem_id}: {e}")
                error_count += 1
                conn.rollback()
        else:
            error_count += 1

    conn.close()
    print(f"\nDone! Imported {new_count} solutions ({error_count} errors)")


def check_for_updates():
    """Check for upstream changes."""
    # Sync repo first
    if not sync_repo():
        print("Failed to sync repository")
        return

    conn = init_database()
    cursor = conn.cursor()

    # Get our stored metadata
    cursor.execute("SELECT problem_id, file_hash FROM source_metadata")
    our_data = {row['problem_id']: row['file_hash'] for row in cursor.fetchall()}

    # Get current files from local repo
    solution_files = get_all_solution_files()

    new_files = []
    changed_files = []

    for sf in solution_files:
        if sf.problem_id not in our_data:
            new_files.append(sf.problem_id)
        else:
            # Check if content changed
            content = read_solution_content(sf)
            if content:
                current_hash = sha256_hash(content)
                if current_hash != our_data[sf.problem_id]:
                    changed_files.append(sf.problem_id)

    print(f"\nSummary:")
    print(f"  Our database: {len(our_data)} problems")
    print(f"  Upstream: {len(solution_files)} problems")
    print(f"  New: {len(new_files)}")
    print(f"  Changed: {len(changed_files)}")

    if new_files and len(new_files) <= 10:
        print(f"\nNew problems:")
        for pid in new_files:
            print(f"  + {pid}")

    if changed_files and len(changed_files) <= 10:
        print(f"\nChanged problems:")
        for pid in changed_files:
            print(f"  ~ {pid}")

    # Check needs_review count
    cursor.execute("SELECT COUNT(*) FROM enrichments WHERE needs_review = 1")
    needs_review = cursor.fetchone()[0]
    if needs_review:
        print(f"\n{needs_review} problems flagged for review")

    conn.close()


def show_stats():
    """Show database statistics."""
    if not DB_PATH.exists():
        print("Database not found. Run import first.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM problems")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM solutions")
    total_solutions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM enrichments WHERE needs_review = 1")
    needs_review = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM enrichments WHERE explanation != ''")
    with_explanations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM enrichments WHERE difficulty IS NOT NULL")
    with_difficulty = cursor.fetchone()[0]

    cursor.execute("""
        SELECT difficulty, COUNT(*) as count
        FROM enrichments
        WHERE difficulty IS NOT NULL
        GROUP BY difficulty
    """)
    by_difficulty = {row['difficulty']: row['count'] for row in cursor.fetchall()}

    print(f"Database Statistics:")
    print(f"  Total problems: {total}")
    print(f"  Total solution approaches: {total_solutions}")
    print(f"  With difficulty set: {with_difficulty}/{total}")
    if by_difficulty:
        for diff in ['Easy', 'Medium', 'Hard']:
            if diff in by_difficulty:
                print(f"    {diff}: {by_difficulty[diff]}")
    print(f"  With explanations: {with_explanations}")
    print(f"  Needs review: {needs_review}")

    conn.close()


def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(__doc__)
        return

    if '--check' in args:
        check_for_updates()
    elif '--stats' in args:
        show_stats()
    elif '--update' in args:
        import_all_solutions(update_only=True)
    else:
        import_all_solutions(update_only=False)


if __name__ == "__main__":
    main()
