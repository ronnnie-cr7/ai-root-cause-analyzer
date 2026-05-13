import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "./data/analysis_memory.db"

def init_db():
    os.makedirs("./data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            log_type TEXT,
            severity TEXT,
            root_cause TEXT,
            fix_suggestions TEXT,
            confidence_score INTEGER,
            rag_source TEXT,
            loop_count INTEGER,
            raw_logs TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_analysis(result: dict, raw_logs: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses 
        (timestamp, log_type, severity, root_cause, fix_suggestions, confidence_score, rag_source, loop_count, raw_logs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        result.get("log_type", "unknown"),
        result.get("severity", "unknown"),
        result.get("root_cause", ""),
        result.get("fix_suggestions", ""),
        result.get("confidence_score", 0),
        result.get("rag_source", "chromadb"),
        result.get("loop_count", 1),
        raw_logs[:500]
    ))
    conn.commit()
    conn.close()
    print(">> Analysis saved to memory.")

def get_recent_analyses(limit: int = 5):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, log_type, severity, root_cause, confidence_score, rag_source
        FROM analyses
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    analyses = []
    for row in rows:
        analyses.append({
            "timestamp": row[0],
            "log_type": row[1],
            "severity": row[2],
            "root_cause": row[3][:200],
            "confidence_score": row[4],
            "rag_source": row[5]
        })
    return analyses

def get_stats():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM analyses")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(confidence_score) FROM analyses")
    avg_confidence = cursor.fetchone()[0]
    cursor.execute("SELECT severity, COUNT(*) FROM analyses GROUP BY severity")
    severity_counts = dict(cursor.fetchall())
    conn.close()

    return {
        "total_analyses": total,
        "avg_confidence": round(avg_confidence, 1) if avg_confidence else 0,
        "severity_counts": severity_counts
    }