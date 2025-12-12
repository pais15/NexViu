from dataManager import db  # مهم!
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from pyrogram import filters
from pyrogram import Client
from imports import *
from dotenv import load_dotenv
processed= set()
load_dotenv()


async def get_markup(user_id: int) -> ReplyKeyboardMarkup:
    buttons = []

    try:
        user = await db.select("users", columns=["work"], where={"userID": str(user_id)})
        if user and user[0].get("work") and "play" in user[0]["work"]:
            buttons.append([KeyboardButton("📢 کانال‌ها و گروه‌های من")])

        buttons.append([KeyboardButton("🚀 ثبت تبلیغ جدید")])
        buttons.append([KeyboardButton("💸 نمایش تبلیغ و کسب درآمد")])

        # ------------------------
        # دکمه‌های مالی و پشتیبانی
        # ------------------------
        buttons.append([KeyboardButton("💰 کیف پول و تراکنش‌ها"), KeyboardButton("🆘 پشتیبانی و راهنما")])

        # ------------------------
        # دکمه‌های درباره و همکاری
        # ------------------------
        buttons.append([KeyboardButton("💜 درباره NexViu"), KeyboardButton("🤝 همکاری با ما")])

        channel_ids = await db.select("channel", columns=["userID"])
        post_ids = await db.select("post", columns=["userID"])
        channel_ids = channel_ids if channel_ids else []
        post_ids = post_ids if post_ids else []
        all_special = {item["userID"] for item in channel_ids + post_ids if item.get("userID")}

        if str(user_id) in all_special:
            buttons.append([KeyboardButton("آمار، گزارش و رویدادها")])

        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    except Exception as e:
        print(f"خطا در ساخت منو برای کاربر {user_id}: {e}")
        return ReplyKeyboardMarkup([[KeyboardButton('🏠 خانه')]], resize_keyboard=True)


async def _dont_exists_filter(_, __, m):
    return not await db.exists("users", {"userID": str(m.from_user.id)})

async def _exists_filter(_, __, m):
    return await db.exists("users", {"userID": str(m.from_user.id)})

def not_bot_message(_, __, m: Message):
    return not m.from_user.is_bot

not_bot = filters.create(not_bot_message)
dont_exists_filter = filters.create(_dont_exists_filter)
exists_filter = filters.create(_exists_filter)

ADMIN = "7979574575" 

app = Client(
    "NexViu",
    bot_token=os.getenv("TOKEN"),
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    workdir="/app",
    in_memory=False
)
# --------- منوی اصلی ادمین ---------
admin_markup = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🚀 ثبت تبلیغ جدید"), KeyboardButton("💸 نمایش تبلیغ و کسب درآمد")],
        [KeyboardButton("📢 کانال‌ها و گروه‌های من")],
        [KeyboardButton("👥 لیست کاربران"), KeyboardButton("🛑 حذف کاربران متخلف")],
        [KeyboardButton("📊 گزارش و آمار سیستم")],
        [KeyboardButton("💰 تنظیم هزینه تبلیغات"), KeyboardButton("💵 تنظیم درآمد منتشرکنندگان")],
        [KeyboardButton("💳 شارژ حساب / امور مالی")],
        [KeyboardButton("🆘 پشتیبانی و راهنما")],
        [KeyboardButton("💜 درباره NexViu"), KeyboardButton("🤝 همکاری با ما")],
    ],
    resize_keyboard=True
)

SITE = 'https://www.Nexviu.ir'

HI_MEMBER = HI_MEMBER = """🌟 **خوش‌آمدید به NexViu!**

NexViu یک سیستم کامل تبلیغاتی و درآمدزایی در تلگرام است — ساده، امن و قابل تنظیم برای هر نوع کسب‌وکار یا ناشر.

**🔹 امکانات اصلی**
• **تبلیغات هدفمند** — انتخاب دسته‌بندی و هدف‌گذاری دقیق  
• **زمان‌بندی هوشمند** — ارسال در تاریخ و ساعت دلخواه با دقت بالا  
• **کسب درآمد برای ناشران** — پرداخت به‌ازای انتشار و بازدید واقعی  
• **مدیریت مالی آسان** — شارژ و برداشت با پیگیری تراکنش‌ها  
• **گزارش‌ها و آمار دقیق** — خروجی قابل‌اشتراک و تحلیل عملکرد

**🔧 مدیریت و امنیت**
• کنترل کامل بر تأیید پست‌ها و حذف خودکار پس از رسیدن به هدف بازدید  
• جلوگیری از اسپم و سیستم اعطای پورسانت برای دعوت‌های موفق

**🚀 شروع سریع**
برای ادامه کافیست دستور زیر را ارسال کنید:
`/start`

اگر سوال یا مشکلی دارید، از دکمه‌ی پشتیبانی استفاده کنید — تیم پشتیبانی در دسترس است.

💜 با NexViu رشد کنید؛ تبلیغ هوشمند، درآمد واقعی.
"""