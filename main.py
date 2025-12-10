from pyrogram import Client, filters
from imports import *

load_dotenv()

app = Client(
    "NexViu",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    workdir="/app", 
    in_memory=False
)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("سلام! حالا دیگه هیچ وقت فلود نمی‌شم 🎉")

if __name__ == "__main__":
    app.run() 

