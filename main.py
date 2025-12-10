from pyrogram import Client, filters, idle
from dotenv import load_dotenv
import os

load_dotenv()

app = Client(
    "NexViu",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("TOKEN"),
    workdir="/app", 
    in_memory=False
)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("سلام! حالا دیگه هیچ وقت فلود نمی‌شم 🎉")

async def main():
    print("در حال استارت ربات...")
    await app.start()
    print("ربات با موفقیت استارت شد و آنلاین است!")
    await idle()
    print("در حال خاموش کردن ربات...")
    await app.stop()

if __name__ == "__main__":
    app.run(main()) 
