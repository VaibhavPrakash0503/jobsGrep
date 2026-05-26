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


def _format_job(job: dict) -> str:
    return (
        f"🆕 <b>{job['title']}</b>\n"
        f"🏢 {job['company']}\n"
        f"📍 {job['location']}\n"
        f"🌐 {job['source'].capitalize()}\n"
        f"📅 {job['date_posted']}\n"
        f"🔗 <a href='{job['url']}'>Apply Here</a>"
    )


async def notify(jobs: list[dict]) -> None:
    if not jobs:
        logger.info("[Notify] No new jobs to send")
        return

    bot = Bot(token=Config.telegram_token)

    # send header message first
    header = f"🔍 <b>Job Hunt</b> — {len(jobs)} new internship(s) found"

    await _send_message(bot, header)
    for job in jobs:
        try:
            message = _format_job(job)
            await _send_message(bot, message)
        except Exception as e:
            logger.warning(f"[Notify] Failed to send job {job['id']}: {e}")
    logger.info(f"[Notify] Sent {len(jobs)} jobs to Telegram")
