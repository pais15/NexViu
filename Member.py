from Const import *

@app.on_message(exists_filter & filters.text_filter("📢 کانال‌ها و گروه‌های من"))
async def my_channels(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text_filter("🚀 ثبت تبلیغ جدید"))
async def new_advertisement(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text_filter("💸 نمایش تبلیغ و کسب درآمد"))
async def show_advertisement(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text_filter("💰 کیف پول و تراکنش‌ها"))
async def wallet_and_transactions(client, m: Message):
    pass


@app.on_message(exists_filter & filters.text_filter("🆘 پشتیبانی و راهنما"))
async def support_and_guide(client, m: Message):
    pass


@app.on_message(filters.text_filter("💜 درباره NexViu"))
async def about_nexviu(client, m: Message):
    await m.reply(HI_MEMBER)


@app.on_message(filters.text_filter("🤝 همکاری با ما"))
async def collaborate_with_us(client, m: Message):
    pass


@app.on_message(filters.text_filter("ℹ️ آمار، گزارش و رویدادها"))
async def stats_reports_events(client, m: Message):
    pass