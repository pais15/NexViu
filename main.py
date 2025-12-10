from pyrogram import Client, filters
from imports import *

load_dotenv()

db_connect = {
    "user": os.getenv("USERDB"),
    "password": os.getenv("PDB"),
    "host": os.getenv("HOSTDB"),
    "port": os.getenv("PORTDB"),
    "database": os.getenv("NAMEDB"),
}
db = Database(**db_connect)
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