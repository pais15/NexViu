from pyrogram import Client, filters
import asyncio, os
from pyrogram import idle

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
    print("در حال راه‌اندازی ربات...")
    await app.start()
    print("ربات در حال اجراست...")
    await idle()
    print("در حال توقف ربات...")
    await app.stop()
    print("ربات متوقف شد.")

if __name__ == "__main__":
    asyncio.run(main())
