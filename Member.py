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
1️⃣ لینک زیر رو برای **دوستات** بفرست
2️⃣ اونا **ثبت‌نام** کنن  
3️⃣ **تو + اونا = سود دوطرفه!** 🚀

⚡ **نکته طلایی:** وقتی دوستت فعال بشه، پاداشت فوری واریز میشه!

🌟 [**فقط با یک کلیک شروع کن!**]({url})

**🚀 پول در انتظارته! فرصت و از دست نده! 💰**''')


@app.on_message(exists_filter & filters.regex(r"^ℹ️ آمار، گزارش و رویدادها$"))
async def stats_reports_events(client: Client, m: Message):
    user_info = await db.select('users', ['userID', 'name', 'family', 'card'], {'userID': str(m.chat.id)})
    userID = user_info[0]['userID']

    default_user = await client.get_users(m.chat.id)

    full_name_db = f"{user_info[0]['name'] or ''} {user_info[0]['family'] or ''}".strip()
    display_name = full_name_db if full_name_db else default_user.first_name
    userName = f"[{display_name}](tg://user?id={userID})"

    card = user_info[0]['card'] or 'تعریف نشده'

    wallet = await db.select('wallet', ['coins'], {'userID': userID})
    coins = wallet[0]['coins']

    posts = await db.select('post', ['postID'], {'userID': userID})

    text = f"""
**👤 اطلاعات کاربر**
- نام: {userName}
- موجودی: **{coins:,} تومان**
- کارت بانکی: `{card}`

"""

    channels = await db.select('channel', ['title', 'link'], {'userID': userID})
    if channels:
        text += "**📢 کانال‌ها و گروه‌های ثبت‌شده:**\n"
        for ch in channels:
            title = ch["title"]
            link = ch["link"]
            text += f"- [{title}]({link})\n"
        text += "\n"

    if posts:
        text += "**📝 پست‌های ارسال‌شده:**\n"
        post_lines = []

        for post in posts:
            postID = post['postID']
            sent_posts = await db.select(
                'create_post', 
                ['channelID', 'textID', 'catgID', 'status'], 
                {'postID': postID}
            )

            for num, sent in enumerate(sent_posts, start=1):
                if sent['status'] == 'sent':
                    channel = await db.select('channel', ['link'], {'channelID': sent['channelID']})
                    link = channel[0]['link']
                    post_lines.append(f"- پست **{num}** → [مشاهده در کانال]({link})")

        if post_lines:
            text += "\n".join(post_lines)

    await m.reply(text, parse_mode="markdown")