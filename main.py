from pyrogram import Client, filters
from dotenv import load_dotenv
import asyncio, os

load_dotenv()

app = Client(
    "NexViu",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("TOKEN")
)

@app.on_message(filters.command("start"))
async def start(_, message):
    print(f"Received /start from user {message.from_user.id}")
    await message.reply("سلام! من ربات تستی هستم. چطور می‌تونم کمکت کنم؟")

async def main():
    print("Starting bot...")
    await app.start()
    print("Bot started.")
    await asyncio.Event().wait() 


if __name__ == "__main__":
    asyncio.run(main())



