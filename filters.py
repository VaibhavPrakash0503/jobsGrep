import logging
from config import Config

logger = logging.getLogger(__name__)


def filter_jobs(jobs: list[dict]) -> list[dict]:
    filtered = []

    for job in jobs:
        title = job["title"].lower()
        description = job["description"].lower()
        location = job["location"].lower()
        company = job["company"].lower()

        # 1 — exclude senior roles from title
        if any(kw in title for kw in Config.exclude_keywords):
            continue

        # 2 — exclude service based companies
        if any(kw in company for kw in Config.exclude_companies):
            continue

        # 3 — must be remote
        is_remote = any(
            kw in location or kw in description for kw in Config.allowed_locations
        )
        if not is_remote:
            continue

        # 4 — must match allowed roles
        is_valid_role = any(kw in title for kw in Config.allowed_roles)
        if not is_valid_role:
            continue

        # 5 — tech stack is optional (do not filter out if missing)

        # 6 — must have fresher signal
        has_fresher_signal = any(
            kw in title or kw in description for kw in Config.experience_keywords
        )
        if not has_fresher_signal:
            continue

        filtered.append(job)

    logger.info(f"[Filter] {len(filtered)} jobs passed out of {len(jobs)}")
    return filtered
