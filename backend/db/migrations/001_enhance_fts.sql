-- Migration: Enhance FTS5 search with more fields and BM25 ranking
-- Run this to upgrade the search capabilities

-- Drop old FTS table and triggers
DROP TRIGGER IF EXISTS problems_ai;
DROP TRIGGER IF EXISTS problems_ad;
DROP TRIGGER IF EXISTS problems_au;
DROP TABLE IF EXISTS problems_fts;

-- Create enhanced FTS5 table with more searchable fields
-- Using porter tokenizer for stemming (search -> searching, searches)
CREATE VIRTUAL TABLE problems_fts USING fts5(
    problem_id UNINDEXED,  -- Store but don't index
    title,
    topics,                 -- Searchable topics
    approaches,             -- Solution approach names
    tokenize='porter unicode61 remove_diacritics 1'
);

-- Populate FTS table with existing data
INSERT INTO problems_fts (problem_id, title, topics, approaches)
SELECT
    p.problem_id,
    p.title,
    COALESCE(
        REPLACE(REPLACE(REPLACE(e.topics, '[', ''), ']', ''), '"', ''),
        ''
    ),
    COALESCE(
        GROUP_CONCAT(s.approach_name, ' '),
        ''
    )
FROM problems p
LEFT JOIN enrichments e ON p.problem_id = e.problem_id
LEFT JOIN solutions s ON p.problem_id = s.problem_id
GROUP BY p.problem_id;

-- Create triggers to keep FTS in sync

-- After INSERT on problems
CREATE TRIGGER problems_fts_ai AFTER INSERT ON problems BEGIN
    INSERT INTO problems_fts (problem_id, title, topics, approaches)
    SELECT
        NEW.problem_id,
        NEW.title,
        COALESCE(
            REPLACE(REPLACE(REPLACE(e.topics, '[', ''), ']', ''), '"', ''),
            ''
        ),
        ''
    FROM (SELECT 1)
    LEFT JOIN enrichments e ON e.problem_id = NEW.problem_id;
END;

-- After DELETE on problems
CREATE TRIGGER problems_fts_ad AFTER DELETE ON problems BEGIN
    DELETE FROM problems_fts WHERE problem_id = OLD.problem_id;
END;

-- After UPDATE on problems (title change)
CREATE TRIGGER problems_fts_au AFTER UPDATE ON problems BEGIN
    UPDATE problems_fts
    SET title = NEW.title
    WHERE problem_id = NEW.problem_id;
END;

-- After INSERT/UPDATE on enrichments (topics change)
CREATE TRIGGER enrichments_fts_ai AFTER INSERT ON enrichments BEGIN
    UPDATE problems_fts
    SET topics = REPLACE(REPLACE(REPLACE(NEW.topics, '[', ''), ']', ''), '"', '')
    WHERE problem_id = NEW.problem_id;
END;

CREATE TRIGGER enrichments_fts_au AFTER UPDATE ON enrichments
WHEN OLD.topics != NEW.topics BEGIN
    UPDATE problems_fts
    SET topics = REPLACE(REPLACE(REPLACE(NEW.topics, '[', ''), ']', ''), '"', '')
    WHERE problem_id = NEW.problem_id;
END;

-- After INSERT on solutions (new approach)
CREATE TRIGGER solutions_fts_ai AFTER INSERT ON solutions BEGIN
    UPDATE problems_fts
    SET approaches = (
        SELECT GROUP_CONCAT(approach_name, ' ')
        FROM solutions
        WHERE problem_id = NEW.problem_id
    )
    WHERE problem_id = NEW.problem_id;
END;

-- After DELETE on solutions
CREATE TRIGGER solutions_fts_ad AFTER DELETE ON solutions BEGIN
    UPDATE problems_fts
    SET approaches = COALESCE(
        (SELECT GROUP_CONCAT(approach_name, ' ') FROM solutions WHERE problem_id = OLD.problem_id),
        ''
    )
    WHERE problem_id = OLD.problem_id;
END;
