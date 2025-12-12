from Helper import *
from Const import *
import fcntl, sys

def prevent_double_run():
    lockfile_path = "/tmp/bot.lock"
    lockfile = open(lockfile_path, "w")
    try:
        fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("✔ Bot lock acquired. Only one instance running.")
    except BlockingIOError:
        print("❌ Another instance detected! Exiting...")
        sys.exit()

prevent_double_run()


@app.on_message(filters.private & filters.command("start"))
async def start(client:Client, m: Message):
    m.chat.id = str(m.chat.id)
    if not await db.exists('users', {'userID': m.chat.id}):
        await db.insert('users', {
            'userID': m.chat.id,
            'username': m.from_user.username or None,
                'name': None,
                'family': None,
                'work': None,
                'move': None,
                'role': 'member' if m.chat.id != ADMIN else 'admin',
                'card': None,
                'userTextID': None,
                'botTextID': None
            })
        await db.insert('wallet', {
            'userID': m.chat.id,
            'coins': 1000,
            'charges':[],
            'withdraws':[]
        })
        if m.chat.id != ADMIN:
            await process_url_command(m)
            await m.reply(
                HI_MEMBER,
                reply_markup= await get_markup(m.chat.id)
            )
        else:
            await m.reply(
            '''👑 **سلام رئیس NexViu!**\n\n🔧 **آماده مدیریت کاربرا و تنظیم ربات؟**\n🚀 **بزن بریم!**''',
            reply_markup=admin_markup,
        )   
    else:
        if m.chat.id != ADMIN:
            user_data = await db.select('users', ['move', 'name'], {'userID': m.chat.id})
            move = user_data[0]['move'] if user_data else None
            name = user_data[0]['name'] if user_data else None

            if move is not None:
                await m.reply(
                    '''⚠️ **یه لحظه صبر کن!**\n\n🔄 **اول کار قبلیتو تموم کن!**'''
                )
            else:
                name = name if name else "دوست عزیز"
                await m.reply(
                    f'''🌞 **سلام {name}!**\n\n🚀 **امروز چه برنامه‌ای داری؟**\n👇 **یه گزینه انتخاب کن!**''',
                    reply_markup=await get_markup(m.chat.id)
                )  
        else:
            await m.reply(
            '''👑 **سلام رئیس NexViu!**\n\n🔧 **آماده مدیریت کاربرا و تنظیم ربات؟**\n🚀 **بزن بریم!**''',
            reply_markup=admin_markup,
        )


@app.on_message(filters.private &  ~filters.command("start") & dont_exists_filter & not_bot)
async def dont_exists(client:Client, m:Message):
    await m.reply(
        '''🎉 **خوش اومدی! ولی...**
🔐 **اول باید ثبت‌نام کنی!**
👇 فقط `/start` بزن تا شروع کنیم! 🚀''',
    )


@app.on_message(filters.private & exists_filter & filters.regex(r"^🏠 خانه$"))
async def go_home(client:Client, m: Message):
    m.chat.id = str(m.chat.id)
    user_data = await db.select('users', ['move', 'name'], {'userID': m.chat.id})
    move = user_data[0]['move'] if user_data else None
    name = user_data[0]['name'] if user_data else None
    name = name if name else "دوست عزیز"
    await db.update('users', {'move': None}, {'userID': m.chat.id})
    if m.chat.id == ADMIN:
        await m.reply(
            '''👑 **سلام رئیس NexViu!**\n\n🔧 **آماده مدیریت کاربرا و تنظیم ربات؟**\n🚀 **بزن بریم!**''',
            reply_markup=admin_markup,
        )
    else:
        await m.reply(
                f'''🌞 **سلام {name}!**\n\n🚀 **امروز چه برنامه‌ای داری؟**\n👇 **یه گزینه انتخاب کن!**''',
                reply_markup=await get_markup(m.chat.id)
        )

from Member import *
from Admin import *
from moves import *

@app.on_message(filters.private &  exists_filter & not_bot)
async def generic_handler(client:Client, m: Message):
    await m.reply('''🤔 **این دستور رو ندارم!**

👇 **از دکمه‌های زیر بزن:** 💰📢👥🏠''', reply_markup=await get_markup(str(m.chat.id)))


async def on_startup():
    """هر چیزی که قبل از روشن شدن ربات باید انجام بشه اینجا می‌نویسه"""
    print("در حال اتصال به دیتابیس...")
    await db.connect()
    print("دیتابیس با موفقیت وصل شد!")
    await app.start()
    
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(on_startup())