from Helper import *
from Const import *

def move_required(move_name: str):
    async def checker(_, __, m):
        user = await db.select('users', ['move'], {'userID': str(m.from_user.id)})
        return user and user[0].get('move') == move_name
    return filters.create(checker)


@app.on_message(move_required('support'))
async def handle_moves(client: Client, m: Message):
    try:
        if getattr(m, "media", None):
            original_caption = (m.caption or "").strip()
            new_caption = f"{m.chat.id}: {original_caption}".strip()
            await client.copy_message(
                chat_id=int(ADMIN),
                from_chat_id=m.chat.id,
                message_id=m.id,
                caption=new_caption if new_caption else None
            )
        else:
            text = (m.text or m.caption or "").strip()
            new_text = f"{m.chat.id}: {text}" if text else f"{m.chat.id}:"
            await client.send_message(chat_id=int(ADMIN), text=new_text)

    except Exception as e:
        print("Error while sending to admin:", e)
        await m.reply("❌ مشکلی پیش آمد، پیام شما ارسال نشد. دوباره تلاش کن یا بعداً تماس بگیر.")
        return

    await m.reply(
        "✅ **پیامت به پشتیبانی ارسال شد!**\n\nتیم ما در اسرع وقت پاسخ خواهد داد. لطفاً صبور باش! 🙏",
        parse_mode="markdown"
    )
