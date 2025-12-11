import asyncio
from Helper import process_url_command
from Const import app, db, ADMIN, admin_markup, get_markup, dont_exists_filter, exists_filter
from pyrogram import filters
from pyrogram.types import Message

@app.on_message(filters.private & filters.command("start"))
async def start(client, m: Message):
    user_id = str(m.from_user.id)

    # پردازش لینک دعوت فقط اگر پارامتر داشته باشد
    if len(m.command) > 1:
        fake_message = m
        fake_message.text = f"/start {m.command[1]}"
        await process_url_command(fake_message)

    if user_id == ADMIN:
        await m.reply("سلام رئیس NexViu!", reply_markup=admin_markup)
        return

    if not await db.exists('users', {'userID': user_id}):
        await db.insert('users', {
            'userID': user_id,
            'name': None,
            'family': None,
            'work': None,
            'move': None,
            'role': 'member',
            'card': None,
            'userTextID': None,
            'botTextID': None
        })
        await m.reply(
            "خوش اومدی به NexViu!\nیه گزینه انتخاب کن و شروع کنیم!",
            reply_markup=await get_markup(int(user_id))
        )
    else:
        user = await db.select('users', ['move', 'name'], {'userID': user_id})
        move = user[0]['move'] if user else None
        name = user[0]['name'] if user else "دوست عزیز"

        if move:
            await m.reply("اول کار قبلیتو تموم کن!")
        else:
            await m.reply(
                f"سلام {name}!\nامروز چه برنامه‌ای داری؟",
                reply_markup=await get_markup(int(user_id))
            )

@app.on_message(filters.private & ~filters.command("start") & dont_exists_filter)
async def dont_exists(client, m: Message):
    await m.reply("اول باید ثبت‌نام کنی!\nفقط /start بزن 🚀")

@app.on_message(filters.private & filters.text == "خانه" & exists_filter)
async def go_home(client, m: Message):
    user_id = str(m.from_user.id)
    await db.update('users', {'move': None}, {'userID': user_id})
    await m.reply("به خانه خوش اومدی!", reply_markup=await get_markup(int(user_id)))

from Member import *
from Admin import *
from moves import *

@app.on_message(filters.private & exists_filter)
async def catch_all(client, m: Message):
    await m.reply("این دستور رو ندارم!\nاز دکمه‌های پایین استفاده کن 👇",
                  reply_markup=await get_markup(m.from_user.id))

async def main():
    await db.connect()
    print("دیتابیس متصل شد")
    await app.start()
    print("ربات شروع شد")
    await asyncio.Event().wait()  # نگه داشتن ربات زنده

if __name__ == "__main__":
    asyncio.run(main())