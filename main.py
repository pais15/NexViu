from Const import *


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("سلام! حالا دیگه هیچ وقت فلود نمی‌شم 🎉")

if __name__ == "__main__":
    app.run()