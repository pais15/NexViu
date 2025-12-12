from Const import *

@app.on_message(exists_filter & filters.regex(r"^📢 کانال‌ها و گروه‌های من$"))
async def my_channels(client:Client, m: Message):
    pass


@app.on_message(exists_filter & filters.regex(r"^🚀 ثبت تبلیغ جدید$"))
async def new_advertisement(client:Client, m: Message):
    pass


@app.on_message(exists_filter & filters.regex(r"^💸 نمایش تبلیغ و کسب درآمد$"))
async def show_advertisement(client:Client, m: Message):
    pass


@app.on_message(exists_filter & filters.regex(r"^💰 کیف پول و تراکنش‌ها$"))
async def wallet_and_transactions(client:Client, m: Message):
    pass


@app.on_message(exists_filter & filters.regex(r"^🆘 پشتیبانی و راهنما$"))
async def support_and_guide(client:Client, m: Message):
    m.chat.id = str(m.chat.id)
    await m.reply(
        '''🆘 **پشتیبانی و راهنما**\n\nاگر سوالی داری یا به کمک نیاز داری، تیم پشتیبانی ما اینجاست تا کمکت کنه!\n\n📩 **برای ارتباط با پشتیبانی، از دکمه زیر استفاده کن:**''',
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton('🏠 خانه')]],
            resize_keyboard=True
        )
    )
    await db.update('users', {'move': 'support'}, {'userID': m.chat.id})


@app.on_message(exists_filter & filters.regex(r"^💜 درباره NexViu$"))
async def about_nexviu(client:Client, m: Message):
    await m.reply(HI_MEMBER)


@app.on_message(exists_filter & filters.regex(r"^🤝 همکاری با ما$"))
async def collaborate_with_us(client:Client, m: Message):
    url = f"https://t.me/{BOT_USERNAME}?start={m.chat.id}"
    await m.reply(f'''🎉 **سلام! آماده *درآمد میلیونی* هستی؟** 💸

🔥 **فقط ۳ قدم ساده:**
1️⃣ لینک زیر رو برای *دوستات* بفرست
2️⃣ اونا *ثبت‌نام* کنن  
3️⃣ **تو + اونا = سود دوطرفه!** 🚀

⚡ **نکته طلایی:** وقتی دوستت *فعال* بشه، *پاداشت* فوری واریز میشه!

🌟 **لینک *خاص* تو:**
{url}

**🚀 همین حالا شروع کن! 💰**''')


@app.on_message(exists_filter & filters.regex(r"^ℹ️ آمار، گزارش و رویدادها$"))
async def stats_reports_events(client:Client, m: Message):
    pass