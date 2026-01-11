-- LeetCode Solutions Database Schema
-- Source of truth: kamyu104/LeetCode-Solutions

-- Core problem information (from source)
CREATE TABLE IF NOT EXISTS problems (
    problem_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    leetcode_url TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Source solutions from kamyu104 repo
-- Each problem can have multiple solution approaches
CREATE TABLE IF NOT EXISTS solutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id TEXT NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    approach_name TEXT NOT NULL,
    time_complexity TEXT,
    space_complexity TEXT,
    code TEXT NOT NULL,
    source_hash TEXT NOT NULL,  -- SHA256 of the code for change detection
    fetched_at TEXT DEFAULT (datetime('now')),
    UNIQUE(problem_id, approach_name)
);

-- User enrichments (separate from source data)
CREATE TABLE IF NOT EXISTS enrichments (
    problem_id TEXT PRIMARY KEY REFERENCES problems(problem_id) ON DELETE CASCADE,
    difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),  -- NULL if unknown
    topics TEXT DEFAULT '[]',           -- JSON array of topic strings
    explanation TEXT DEFAULT '',         -- Detailed explanation
    key_insights TEXT DEFAULT '[]',      -- JSON array of insight strings
    edge_cases TEXT DEFAULT '[]',        -- JSON array of edge case strings
    similar_problems TEXT DEFAULT '[]',  -- JSON array of {title, url} objects
    needs_review INTEGER DEFAULT 0,      -- Flag: source changed since last review
    reviewed_at TEXT,                    -- When enrichments were last reviewed
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Track source file metadata for change detection
CREATE TABLE IF NOT EXISTS source_metadata (
    problem_id TEXT PRIMARY KEY REFERENCES problems(problem_id) ON DELETE CASCADE,
    file_hash TEXT NOT NULL,            -- SHA256 of entire source file
    fetched_at TEXT DEFAULT (datetime('now')),
    source_url TEXT NOT NULL
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_solutions_problem_id ON solutions(problem_id);
CREATE INDEX IF NOT EXISTS idx_enrichments_difficulty ON enrichments(difficulty);
CREATE INDEX IF NOT EXISTS idx_enrichments_needs_review ON enrichments(needs_review);

-- Full-text search on problem titles
CREATE VIRTUAL TABLE IF NOT EXISTS problems_fts USING fts5(
    problem_id,
    title,
    content='problems',
    content_rowid='rowid'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS problems_ai AFTER INSERT ON problems BEGIN
    INSERT INTO problems_fts(problem_id, title) VALUES (new.problem_id, new.title);
END;

CREATE TRIGGER IF NOT EXISTS problems_ad AFTER DELETE ON problems BEGIN
    INSERT INTO problems_fts(problems_fts, rowid, problem_id, title)
    VALUES('delete', old.rowid, old.problem_id, old.title);
END;

CREATE TRIGGER IF NOT EXISTS problems_au AFTER UPDATE ON problems BEGIN
    INSERT INTO problems_fts(problems_fts, rowid, problem_id, title)
    VALUES('delete', old.rowid, old.problem_id, old.title);
    INSERT INTO problems_fts(problem_id, title) VALUES (new.problem_id, new.title);
END;
