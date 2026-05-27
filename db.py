import logging
import libsql
from config import Config

logger = logging.getLogger(__name__)


def get_conn():
    if not Config.turso_url or not Config.turso_token:
        raise ValueError("TURSO_URL or TURSO_TOKEN is missing")
    return libsql.connect(database=Config.turso_url, auth_token=Config.turso_token)


def init_db() -> None:
    try:
        conn = get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_jobs (
                id TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                url TEXT,
                source TEXT,
                date_posted TEXT,
                seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        logger.info("[DB] Initialized")
    except Exception as e:
        logger.error(f"[DB] Failed to initialize: {e}")
        raise


def is_seen(job_id: str) -> bool:
    conn = get_conn()
    cursor = conn.execute("SELECT 1 FROM seen_jobs WHERE id = ?", (job_id,))
    return cursor.fetchone() is not None


def save_job(job: dict) -> None:
    conn = get_conn()
    conn.execute(
        """
        INSERT OR IGNORE INTO seen_jobs
        (id, title, company, location, url, source, date_posted)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            job["id"],
            job["title"],
            job["company"],
            job["location"],
            job["url"],
            job["source"],
            job["date_posted"],
        ),
    )
    conn.commit()


def filter_unseen(jobs: list[dict]) -> list[dict]:
    unseen = [job for job in jobs if not is_seen(job["id"])]
    logger.info(f"[DB] {len(unseen)} new jobs out of {len(jobs)}")
    return unseen


def mark_seen(jobs: list[dict]) -> None:
    for job in jobs:
        save_job(job)
    logger.info(f"[DB] Marked {len(jobs)} jobs as seen")
