import logging
from config import Config

logger = logging.getLogger(__name__)


def _score_job(job: dict) -> tuple[int, list[str]]:
    title = job["title"].lower()
    description = job["description"].lower()
    location = job["location"].lower()
    company = job["company"].lower()
    reasons = []
    score = 0

    # hard filters
    if any(kw in title for kw in Config.exclude_keywords):
        return -1, ["senior role"]

    if any(kw in company for kw in Config.exclude_companies):
        return -1, ["service company"]

    is_remote = (
        any(kw in location for kw in Config.allowed_locations)
        or any(kw in description for kw in Config.allowed_locations)
        or any(kw in title for kw in Config.allowed_locations)
    )
    if not is_remote:
        return -1, ["not remote"]

    # role match → +3
    if any(kw in title for kw in Config.allowed_roles):
        score += 3
        reasons.append("role match")

    # stack match — title or description, +3 once only
    has_stack = any(kw in title or kw in description for kw in Config.allowed_stack)
    if has_stack:
        score += 3
        reasons.append("stack match")

    # fresher signal — title or description, +3 once only
    has_fresher = any(
        kw in title or kw in description for kw in Config.experience_keywords
    )
    if has_fresher:
        score += 3
        reasons.append("fresher signal")

    # bonus — multiple stack matches +1
    stack_matches = sum(
        1 for kw in Config.allowed_stack if kw in title or kw in description
    )
    if stack_matches >= 3:
        score += 1
        reasons.append("multi stack")

    return score, reasons


def filter_jobs(jobs: list[dict]) -> list[dict]:
    scored = []

    for job in jobs:
        score, reasons = _score_job(job)

        if score == -1:
            logger.debug(f"DISQUALIFIED: {job['title']} | {reasons[0]}")
            continue

        if score >= Config.min_score:
            job["score"] = score
            job["reasons"] = reasons
            scored.append(job)
            logger.debug(f"PASSED ({score}pts): {job['title']} | {reasons}")
        else:
            logger.debug(f"LOW SCORE ({score}pts): {job['title']}")

    # sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    logger.info(f"[Filter] {len(scored)} jobs passed out of {len(jobs)}")
    return scored
