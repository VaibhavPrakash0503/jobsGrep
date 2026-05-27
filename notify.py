import logging
from telegram import Bot
from telegram.constants import ParseMode
from config import Config

logger = logging.getLogger(__name__)


async def _send_message(bot: Bot, message: str) -> None:
    await bot.send_message(
        chat_id=Config.telegram_chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


def _format_job(index: int, job: dict) -> str:
    reasons = ", ".join(job.get("reasons", []))
    score = job.get("score", "?")
    return (
        f"{index}. <b>{job['title']}</b> — {job['company']}\n"
        f"   📍 {job['location']} | 🌐 {job['source'].capitalize()}\n"
        f"   ⭐ {score}pts | {reasons}\n"
        f"   🔗 <a href='{job['url']}'>Apply Here</a>\n"
    )


async def notify(jobs: list[dict]) -> None:
    if not jobs:
        logger.info("[Notify] No new jobs to send")
        return

    bot = Bot(token=Config.telegram_token)

    # jobs already sorted by score descending from filter.py
    lines = [f"🔍 <b>Job Hunt</b> — {len(jobs)} new internship(s) found\n"]

    for i, job in enumerate(jobs, start=1):
        lines.append(_format_job(i, job))

    message = "\n".join(lines)

    # telegram message limit is 4096 chars
    # split if too long
    if len(message) <= 4096:
        await _send_message(bot, message)
    else:
        # send in chunks
        chunk = [lines[0]]  # always include header
        for line in lines[1:]:
            if sum(len(l) for l in chunk) + len(line) > 4096:
                await _send_message(bot, "\n".join(chunk))
                chunk = []
            chunk.append(line)
        if chunk:
            await _send_message(bot, "\n".join(chunk))

    logger.info(f"[Notify] Sent {len(jobs)} jobs in digest to Telegram")
