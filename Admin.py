from Const import *

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^👥 لیست کاربران$"))
async def list_users(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^🛑 حذف کاربران متخلف$"))
async def delete_offending_users(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^📊 گزارش و آمار سیستم$"))
async def system_reports_stats(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^💰 تنظیم هزینه تبلیغات$"))
async def set_advertisement_cost(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^💵 تنظیم درآمد منتشرکنندگان$"))
async def set_publisher_income(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) & filters.private & filters.regex(r"^💳 شارژ حساب / امور مالی$"))
async def account_recharge_finance(client, m: Message):
    pass


from pyrogram.errors import UserIsBlocked, InputUserDeactivated, ChatWriteForbidden
from pyrogram.enums import ParseMode

@app.on_message(filters.private & filters.user(ADMIN))
async def admin_reply_support(c, m: Message):

    # پیام باید ریپلای باشد
    if not m.reply_to_message:
        return
    
    # پیام ریپلای‌شده باید فوروارد شده باشد
    fwd = m.reply_to_message
    if not (fwd.forward_from or fwd.forward_from_chat):
        return await m.reply("❗️ این پیام، پاسخ به یک پیام فوروارد شده نیست.", quote=True)

    target = fwd.forward_from or fwd.forward_from_chat
    target_id = target.id
    target_name = (
        fwd.forward_from_chat.title if fwd.forward_from_chat else
        f"{fwd.forward_from.first_name or ''} {fwd.forward_from.last_name or ''}".strip() or "کاربر"
    )

    try:
        await c.send_message(
            chat_id=target_id,
            text=m.text or m.caption or "📨 پیام جدید از طرف پشتیبانی",
            reply_to_message_id=fwd.forward_from_message_id
        )

        await m.reply(
            f"✅ پاسخ با موفقیت برای "
            f"<a href='tg://user?id={target_id}'>{target_name}</a> ارسال شد! 🎯",
            parse_mode=ParseMode.HTML,
            quote=True
        )

    except UserIsBlocked:
        await m.reply(f"⛔️ {target_name} ربات را بلاک کرده است.", quote=True)

    except InputUserDeactivated:
        await m.reply(f"⚠️ حساب {target_name} حذف شده است.", quote=True)

    except Exception as e:
        await m.reply(
            f"🚫 خطا رخ داد:\n<code>{str(e)[:100]}</code>",
            parse_mode=ParseMode.HTML,
            quote=True
        )
