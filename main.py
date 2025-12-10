from pyrogram import Client, filters
import asyncio, os

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
    await asyncio.Event().wait()   # ربات همیشه روشن می‌ماند

if __name__ == "__main__":
    asyncio.run(main())
