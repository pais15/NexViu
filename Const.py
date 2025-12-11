from dataManager import *

load_dotenv()

async def get_markup(user_id: int) -> ReplyKeyboardMarkup:
    """
    ساخت منوی کاربر بهینه برای Pyrogram
    db: کلاس Database async (مثل کلاس Database ما)
    """

    buttons = []

    try:
        # ------------------------
        # دکمه‌های اصلی
        # ------------------------
        user = await db.select("users", columns=["work"], where={"userID": user_id})
        if user and user[0]["work"]:
            if "play" in user[0]["work"]:
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

        # ------------------------
        # دکمه ویژه کاربران خاص
        # ------------------------
        # یک کوئری برای گرفتن همه id ها در یک بار
        special_ids = await db.select("channel", columns=["userID"])
        special_ids += await db.select("post", columns=["userID"])

        if any(item["userID"] == user_id for item in special_ids):
            buttons.append([KeyboardButton("ℹ️ آمار، گزارش و رویدادها")])

        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    except Exception as e:
        print(f"خطا در ساخت منو برای کاربر {user_id}: {e}")
        return ReplyKeyboardMarkup([], resize_keyboard=True)

async def _dont_exists_filter(_, __, m: Message):
    return not await db.exists('users', {'userID': str(m.chat.id)})

async def _exists_filter(_, __, m: Message):
    return await db.exists('users', {'userID': str(m.chat.id)})

async def _move_filter(_, __, m: Message, move):
    return await db.select('users', ['move'], {'userID': str(m.chat.id)})[0]['move'] == move

app = Client(
    "NexViu",
    bot_token=os.getenv("BOT_TOKEN"),
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    workdir="/app", 
    in_memory=False
)

db_connect = {
    "user": os.getenv("USERDB"),
    "password": os.getenv("PDB"),
    "host": os.getenv("HOSTDB"),
    "port": os.getenv("PORTDB"),
    "database": os.getenv("NAMEDB"),
}

db = Database(**db_connect)

ADMIN = '7979574575'

dont_exists_filter = filters.create(_dont_exists_filter)
exists_filter = filters.create(_exists_filter)
move_filter = filters.create(_move_filter)

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