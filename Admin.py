from Const import *

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^👥 لیست کاربران$"))
async def list_users(client:Client, m: Message):
    users = await db.select('users', ['userID', 'name', 'family', 'work', 'move', 'card'])
    if not users:
        await m.reply("هیچ کاربری ثبت نشده است.")
        return
    
    message_lines = ["👥 **لیست کاربران ثبت‌شده:**\n"
                     "-------------------------"]
    for user in users:
        userID = user['userID']
        wallet = await db.select('wallet', ['coins'], {'userID': userID})
        coins = wallet[0]['coins'] if wallet else 0
        default_name = await client.get_users(int(userID))
        name = user.get('name', default_name.first_name if default_name.first_name else "ناشناخته")
        line = f"🆔: `{user['userID']}` | نام: {name} | موجودی: {coins} تومان"
        message_lines.append(line)

    await m.reply("\n".join(message_lines))

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^🛑 حذف کاربران متخلف$"))
async def delete_offending_users(client:Client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^📊 گزارش و آمار سیستم$"))
async def system_reports_stats(client:Client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^💰 تنظیم هزینه تبلیغات$"))
async def set_advertisement_cost(client:Client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^💵 تنظیم درآمد منتشرکنندگان$"))
async def set_publisher_income(client:Client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^💳 شارژ حساب / امور مالی$"))
async def account_recharge_finance(client:Client, m: Message):
    pass


from pyrogram.errors import UserIsBlocked, InputUserDeactivated, ChatWriteForbidden
from pyrogram.enums import ParseMode

@app.on_message(filters.private & filters.user(int(ADMIN)) & filters.reply)
async def admin_reply_support(c:Client, m: Message):
    if not m.reply_to_message:
        return

    text = m.reply_to_message.caption or m.reply_to_message.text or ""

    target = text.split(':')[0].strip()
    target_id = int(target) if target.isdigit() else None
    if not target_id:
        await m.reply("⚠️ نمی‌تونم گیرنده پیام رو پیدا کنم.")
        return

    user = await c.get_users(target_id)
    parts = [ (getattr(user, "first_name", "") or "").strip(),
          (getattr(user, "last_name",  "") or "").strip() ]

    name = " ".join(p for p in parts if p)
    target_name = name or (getattr(user, "username", "") or "") or "کاربر"

    try:
        await c.copy_message(
            chat_id=target_id,
            from_chat_id=m.chat.id,
            message_id=m.id
        )
        await m.reply(
            f"✅ پیام برای "
            f"<a href='tg://user?id={target_id}'>{target_name}</a> ارسال شد!",
            parse_mode=ParseMode.HTML,
            quote=True
        )

    except Exception as e:
        await m.reply(f"⚠️ خطا:\n<code>{e}</code>", parse_mode=ParseMode.HTML)