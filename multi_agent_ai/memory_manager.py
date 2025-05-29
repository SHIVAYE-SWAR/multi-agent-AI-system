import sqlite3
import json
from datetime import datetime

class MemoryManager:
    def __init__(self, db_path="shared_memory.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            format TEXT,
            timestamp TEXT,
            conversation_id TEXT,
            extracted_data TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def log_entry(self, source, fmt, conversation_id, extracted_data: dict):
        timestamp = datetime.utcnow().isoformat()
        extracted_json = json.dumps(extracted_data)
        query = """
        INSERT INTO memory (source, format, timestamp, conversation_id, extracted_data)
        VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (source, fmt, timestamp, conversation_id, extracted_json))
        self.conn.commit()

    def get_conversation_entries(self, conversation_id):
        query = "SELECT * FROM memory WHERE conversation_id = ? ORDER BY timestamp"
        cursor = self.conn.execute(query, (conversation_id,))
        rows = cursor.fetchall()
        results = []
        for row in rows:
            entry = {
                "id": row[0],
                "source": row[1],
                "format": row[2],
                "timestamp": row[3],
                "conversation_id": row[4],
                "extracted_data": json.loads(row[5])
            }
            results.append(entry)
        return results

    def close(self):
        self.conn.close()
