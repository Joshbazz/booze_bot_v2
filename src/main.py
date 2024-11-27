import os
import asyncio
import threading
from claude_scraper import WhiskeyScraper
from discord_bot import WhiskeyBot

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configuration from .env
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Discord bot token
# JSON_FILE_PATH = os.getenv('JSON_FILE_PATH', 'whiskey_data.json')  # Default to 'whiskey_data.json' if not specified
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', 0))  # Convert to int; defaults to 0 if not provided


def run_scraper():
    """
    Run the scraper as a separate thread.
    """
    scraper = WhiskeyScraper()
    scraper.start_scraper(iterations=6, min_sleep=60, max_sleep=90)

async def run_bot():
    """
    Run the Discord bot in an asyncio event loop.
    """
    bot = WhiskeyBot(
        token=DISCORD_TOKEN,
        channel_id=DISCORD_CHANNEL_ID
    )

    await bot.start()


if __name__ == "__main__":
    # Start scraper in a separate thread
    scraper_thread = threading.Thread(target=run_scraper)
    scraper_thread.daemon = True
    scraper_thread.start()

    # Start the Discord bot in the already running event loop
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())  # Schedule the bot as a coroutine
    loop.run_forever()  # Keep the loop running
