from Helper import *
from Member import *
from Admin import *
from Const import *


@app.on_message(filters.command("start") & filters.private)
async def start(client, m: Message):
    if m.chat.id != ADMIN:
        if not await db.exists('users', {'userID': m.chat.id}):
            await db.insert('users', {
                'userID': m.chat.id,
                'name': None,
                'family': None,
                'work': None,
                'move': None,
                'role': 'member',
                'card': None,
                'userTextID': None,
                'botTextID': None
            })
            await process_url_command(m)
            await m.reply(
                '''🌟 **خوش اومدی به NexViu!**\n\n🚀 **آماده‌ای کانالت رو بترکونی؟**\n👇 **یه گزینه انتخاب کن و شروع کنیم!**''',
                reply_markup=await get_markup(m.chat.id)
            )
        else:
            # اول select کامل را await کن
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


@app.on_message()
async def debug_handler(_, m):
    print("MESSAGE RECEIVED:", m.text)
    await m.reply("Received.")

async def main():
    print("در حال اتصال به دیتابیس...")
    await db.connect()                    # ← اول دیتابیس وصل می‌شه
    print("دیتابیس با موفقیت وصل شد!")
    
    print("در حال شروع ربات...")
    await app.start()                     # ← بعد ربات استارت می‌شه
    print("ربات با موفقیت شروع شد!")
    
    # اینجا یک ترفند مهم: دستی dispatcher رو فعال می‌کنیم
    # این خط باعث می‌شه همه هندلرهایی که با @app.on_message تعریف کردی، ثبت بشن
    await app.dispatcher.start()
    
    print("همه هندلرها ثبت شدند. ربات آماده است!")
    print(f"تعداد هندلرهای ثبت‌شده: {len(app.dispatcher.groups.get(0, []))}")
    
    await idle()                          # منتظر پیام‌ها می‌مونه
    print("در حال خاموش شدن...")
    
    await app.dispatcher.stop()
    await app.stop()
    await db.close()
    print("ربات و دیتابیس با موفقیت بسته شدند.")

if __name__ == "__main__":
    asyncio.run(main())
