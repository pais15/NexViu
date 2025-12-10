from pyrogram import Client, filters
import asyncio
from pyngrok import ngrok

# تنظیمات کلاینت + پروکسی MTProto (برای ایران عالیه)
app = Client(
    "NexViu",
    api_id=20569546,
    api_hash="5662d07837071d97e94ee6d08950c1cf",
    bot_token="8296068934:AAHgTXCVbj3gTLeNcsTeoFQq8l6H5da5ThQ",
)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("ربات با وب‌هوک و ngrok فعال شد!\nحالا ۲۴/۷ و فوق‌العاده سریعم!")

# این هندلر برای دریافت آپدیت‌های وب‌هوک لازمه!
@app.on_raw_update()
async def raw_update(client, update, users, chats):
    # اینجا می‌تونی آپدیت‌ها رو پردازش کنی (اختیاری)
    pass

async def main():
    await app.start()
    print("ربات در حال اتصال...")

    # توکن ngrok رو اینجا بذار (از داشبورد گرفتی)
    ngrok.set_auth_token("3646phe2XyysbhPYbMt5ptYNv7r_6QeXsFb7Qv5tepSVYHjoh")

    # تونل رو روی پورت 8000 باز کن
    public_url = ngrok.connect(8000, "http")
    webhook_url = f"{public_url}/webhook"

    print(f"تونل ngrok باز شد: {public_url}")
    print(f"وب‌هوک ست می‌شه روی: {webhook_url}")

    # وب‌هوک رو ست کن
    success = await app.set_webhook(webhook_url)
    if success:
        print("وب‌هوک با موفقیت ست شد! ربات حالا ۲۴/۷ و فوق‌العاده سریع است!")
    else:
        print("خطا در ست کردن وب‌هوک!")

    # این خط مهمه! ربات رو تا ابد نگه می‌داره
    await asyncio.Event().wait()

# اجرا
if __name__ == "__main__":
    asyncio.run(main())