from pyrogram import Client, filters
from dotenv import load_dotenv
import asyncio, os
from pyrogram import idle

load_dotenv()

app = Client(
    "NexViu",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("TOKEN")
)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("سلام! من ربات تستی هستم. چطور می‌تونم کمکت کنم؟")

async def main():
    await app.start()
    print("ربات با موفقیت استارت شد و در حال polling است...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
