from Helper import *
from Member import *
from Admin import *


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

if __name__ == "__main__":
    import asyncio
    asyncio.run(db.connect())  # دیتابیس connect
    app.run()                  # تمام handlerها فعال می‌شوند