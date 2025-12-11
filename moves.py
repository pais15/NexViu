from Helper import *
from Const import *

@app.on_message(exists_filter & (filters.text != "🏠 خانه"))
async def Handle_moves(client, m: Message):
    m.chat.id = str(m.chat.id)
    rows = await db.select('users', ['move'], {'userID': m.chat.id})
    if not rows:
        return

    move = rows[0].get('move')
    if move == 'support':
        await m.forward(int(ADMIN))
        await m.reply('''✅ **پیامت به پشتیبانی ارسال شد!**\n\nتیم ما در اسرع وقت پاسخ خواهد داد. لطفاً صبور باش! 🙏''')