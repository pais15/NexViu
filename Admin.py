from Const import *

@app.on_message(filters.text_filter("👥 لیست کاربران"))
async def list_users(client, m: Message):
    pass


@app.on_message(filters.text_filter("🛑 حذف کاربران متخلف"))
async def delete_offending_users(client, m: Message):
    pass


@app.on_message(filters.text_filter("📊 گزارش و آمار سیستم"))
async def system_reports_stats(client, m: Message):
    pass


@app.on_message(filters.text_filter("💰 تنظیم هزینه تبلیغات"))
async def set_advertisement_cost(client, m: Message):
    pass


@app.on_message(filters.text_filter("💵 تنظیم درآمد منتشرکنندگان"))
async def set_publisher_income(client, m: Message):
    pass


@app.on_message(filters.text_filter("💳 شارژ حساب / امور مالی"))
async def account_recharge_finance(client, m: Message):
    pass