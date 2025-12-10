from Const import *


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("سلام! چکاری از دستم بر میاد؟ 🎉")

if __name__ == "__main__":
    app.run()