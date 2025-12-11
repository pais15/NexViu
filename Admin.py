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

@app.on_message(filters.private & filters.forwarded & filters.user(int(ADMIN)))
async def admin_reply_support(c, m: Message):
    if not (m.forward_from or m.forward_from_chat):
        return await m.reply("❗️ منبع پیام پیدا نشد! لطفاً پیام صحیحی فوروارد کنید.", quote=True)

    target = m.forward_from or m.forward_from_chat
    target_id = target.id
    target_name = (
        m.forward_from_chat.title if m.forward_from_chat else
        f"{m.forward_from.first_name or ''} {m.forward_from.last_name or ''}".strip() or "کاربر"
    )

    try:
        await m.forward(chat_id=target_id)

        await m.reply(
            f"✅ پاسخ با موفقیت برای "
            f"<a href='tg://user?id={target_id}'>{target_name}</a> ارسال شد! 🎯\n\n"
            "📨 کاربر پیام را دریافت کرد.\n"
            "🔥 ادمین حرفه‌ای در حال درخشیدنه!",
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