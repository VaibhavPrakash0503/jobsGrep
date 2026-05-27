import logging
from supabase import create_client, Client
from config import Config

logger = logging.getLogger(__name__)


def get_client() -> Client:
    if not Config.supabase_url or not Config.supabase_key:
        raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing")
    return create_client(Config.supabase_url, Config.supabase_key)


def init_db() -> None:
    try:
        client = get_client()
        client.table("seen_jobs").select("id").limit(1).execute()
        logger.info("[DB] Connected to Supabase")
    except Exception as e:
        logger.error(f"[DB] Failed to connect: {e}")
        raise


def is_seen(job_id: str) -> bool:
    client = get_client()
    result = client.table("seen_jobs").select("id").eq("id", job_id).execute()
    return len(result.data) > 0


def save_job(job: dict) -> None:
    client = get_client()
    client.table("seen_jobs").upsert(
        {
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "url": job["url"],
            "source": job["source"],
            "date_posted": job["date_posted"],
        }
    ).execute()


def filter_unseen(jobs: list[dict]) -> list[dict]:
    unseen = [job for job in jobs if not is_seen(job["id"])]
    logger.info(f"[DB] {len(unseen)} new jobs out of {len(jobs)}")
    return unseen


def mark_seen(jobs: list[dict]) -> None:
    for job in jobs:
        save_job(job)
    logger.info(f"[DB] Marked {len(jobs)} jobs as seen")
