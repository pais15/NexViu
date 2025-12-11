from dataManager import *
from Helper import _dont_exists_filter
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

ADMIN = '7979574575'

dont_exists_filter = filters.create(_dont_exists_filter)

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
