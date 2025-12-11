from Const import *

@app.on_message(filters.user(int(ADMIN)) and filters.private and (filters.text == "👥 لیست کاربران"))
async def list_users(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) and filters.private and (filters.text == "🛑 حذف کاربران متخلف"))
async def delete_offending_users(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) and filters.private and (filters.text == "📊 گزارش و آمار سیستم"))
async def system_reports_stats(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) and filters.private and (filters.text == "💰 تنظیم هزینه تبلیغات"))
async def set_advertisement_cost(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) and filters.private and (filters.text == "💵 تنظیم درآمد منتشرکنندگان"))
async def set_publisher_income(client, m: Message):
    pass

@app.on_message(filters.user(int(ADMIN)) and filters.private and (filters.text == "💳 شارژ حساب / امور مالی"))
async def account_recharge_finance(client, m: Message):
    pass


@app.on_message(filters.private and filters.forwarded and filters.user(ADMIN))
def admin_reply_support(client, m: Message):
    original_chat_id = str(m.forward_from_chat.id) if m.forward_from_chat else str(m.forward_from.id)
    client.send_message(
        chat_id=original_chat_id,
        text=f'''💬 **پاسخ پشتیبانی:**\n\n{m.text}'''
    )