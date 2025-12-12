from Helper import *
from Const import *

def move_required(move_name: str):
    async def checker(_, __, m):
        user = await db.select('users', ['move'], {'userID': str(m.from_user.id)})
        return user and user[0].get('move') == move_name
    return filters.create(checker)

@app.on_message(move_required('support'))
async def Handle_moves(client:Client, m: Message):
    sent = await m.forward(int(ADMIN))
    if sent.caption:
        await client.edit_message_caption(sent.chat.id, sent.message_id, caption=f"{m.chat.id}: {sent.caption}")
    elif sent.text:
        await client.edit_message_text(sent.chat.id, sent.message_id, text=f"{m.chat.id}: {sent.text}")

    await m.reply('''✅ **پیامت به پشتیبانی ارسال شد!**\n\nتیم ما در اسرع وقت پاسخ خواهد داد. لطفاً صبور باش! 🙏''')