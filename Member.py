from Const import *

@app.on_message(exists_filter & filters.text == "📢 کانال‌ها و گروه‌های من")
async def my_channels(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text == "🚀 ثبت تبلیغ جدید")
async def new_advertisement(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text == "💸 نمایش تبلیغ و کسب درآمد")
async def show_advertisement(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text == "💰 کیف پول و تراکنش‌ها")
async def wallet_and_transactions(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text == "🆘 پشتیبانی و راهنما")
async def support_and_guide(client, m: Message):
    await m.reply('''🆘 **پشتیبانی و راهنما**\n\nاگر سوالی داری یا به کمک نیاز داری، تیم پشتیبانی ما اینجاست تا کمکت کنه!\n\n📩 **برای ارتباط با پشتیبانی، از دکمه زیر استفاده کن:**''',
                        reply_markup=ReplyKeyboardMarkup(
                            [[KeyboardButton('🏠 خانه')]],
                            resize_keyboard=True
                        )
                         )
    await db.update('users', {'userID': str(m.chat.id)}, {'move': 'support'})


@app.on_message(exists_filter & move_filter('support') & ~filters.text == "🏠 خانه")
async def handle_support_messages(client, m: Message):
    await m.forward(ADMIN)
    await m.reply('''✅ **پیامت به پشتیبانی ارسال شد!**\n\nتیم ما در اسرع وقت پاسخ خواهد داد. لطفاً صبور باش! 🙏**''')


@app.on_message(exists_filter & filters.text == "💜 درباره NexViu")
async def about_nexviu(client, m: Message):
    await m.reply(HI_MEMBER)


@app.on_message(exists_filter & filters.text == "🤝 همکاری با ما")
async def collaborate_with_us(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text_filter("ℹ️ آمار، گزارش و رویدادها"))
async def stats_reports_events(client, m: Message):
    pass