"""Memory management for agent conversations using SQLite."""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from utils.logger import logger

class MemoryManager:
    """Manages conversation memory for each agent using SQLite."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.db_path = Path(f"agents/{agent_name}/memory.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session
                ON conversations(session_id, timestamp)
            """)
            conn.commit()

    def save_message(self, session_id: str, role: str, content: str):
        """Save a message to the conversation history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
                    (session_id, role, content)
                )
                conn.commit()
            logger.info(f"Saved {role} message for session {session_id}")
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
            raise

    def load_context(self, session_id: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Load recent conversation context for a session.

        Args:
            session_id: Session identifier
            limit: Maximum number of messages to load

        Returns:
            List of message dicts with 'role' and 'content'
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT role, content FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (session_id, limit)
                )
                messages = [
                    {"role": row[0], "content": row[1]}
                    for row in cursor.fetchall()
                ]
                # Reverse to get chronological order
                messages.reverse()
                logger.info(f"Loaded {len(messages)} messages for session {session_id}")
                return messages
        except Exception as e:
            logger.error(f"Failed to load context: {e}")
            return []

    def summarize_old_context(self, session_id: str, keep_recent: int = 5):
        """
        Summarize old messages to save tokens (future enhancement).

        For MVP, we just delete old messages beyond the limit.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Count total messages
                cursor = conn.execute(
                    "SELECT COUNT(*) FROM conversations WHERE session_id = ?",
                    (session_id,)
                )
                total = cursor.fetchone()[0]

                if total > keep_recent * 2:  # Only clean when significantly over limit
                    # Delete oldest messages, keeping the most recent ones
                    conn.execute(
                        """
                        DELETE FROM conversations
                        WHERE id IN (
                            SELECT id FROM conversations
                            WHERE session_id = ?
                            ORDER BY timestamp DESC
                            LIMIT -1 OFFSET ?
                        )
                        """,
                        (session_id, keep_recent)
                    )
                    conn.commit()
                    logger.info(f"Cleaned old messages for session {session_id}")
        except Exception as e:
            logger.error(f"Failed to summarize context: {e}")

    def clear_session(self, session_id: str):
        """Delete all messages for a session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "DELETE FROM conversations WHERE session_id = ?",
                    (session_id,)
                )
                conn.commit()
            logger.info(f"Cleared session {session_id}")
        except Exception as e:
            logger.error(f"Failed to clear session: {e}")
