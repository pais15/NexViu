from dataManager import *
load_dotenv()

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

ADMIN = 7979574575

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
        if user and "play" in user[0]["work"]:
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
        special_ids = await db.select("players", columns=["id"])
        special_ids += await db.select("tablighs", columns=["id"])

        if any(item["id"] == user_id for item in special_ids):
            buttons.append([KeyboardButton("ℹ️ آمار، گزارش و رویدادها")])

        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    except Exception as e:
        print(f"خطا در ساخت منو برای کاربر {user_id}: {e}")
        return ReplyKeyboardMarkup([], resize_keyboard=True)
