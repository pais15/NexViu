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


@app.on_message(move_required('search_users'))
async def search_users(client: Client, m: Message):
    query = (m.text or "").strip()
    if not query:
        await m.reply("⚠️ لطفاً یک شناسه کاربری یا آیدی معتبر وارد کن.")
        return

    users = []
    if query.startswith('@'):
        username = query[1:]
        user_record = await db.select('users', ['userID', 'name', 'family', 'work', 'move', 'card'], {'username': username})
        if user_record:
            users.append(user_record[0])
    elif query.isdigit():
        user_record = await db.select('users', ['userID', 'name', 'family', 'work', 'move', 'card'], {'userID': int(query)})
        if user_record:
            users.append(user_record[0])
    else:
        await m.reply("⚠️ لطفاً یک شناسه کاربری یا آیدی معتبر وارد کن.")
        return

    if not users:
        await m.reply("❌ کاربری با این مشخصات پیدا نشد.")
        return

    message_lines = ["👥 **لیست کاربران یافت‌شده:**\n"
                     "-------------------------"]
    for user in users:
        userID = user['userID']
        default_name = await client.get_users(int(userID))
        if user.get('name') and user.get('family'):
                name = f"{user['name']} {user['family']}"
        elif default_name:
            parts = [ (getattr(default_name, "first_name", "") or "").strip(),
                        (getattr(default_name, "last_name",  "") or "").strip() ]
            name = " ".join(p for p in parts if p)
            if not name:
                name = (getattr(default_name, "username", "") or "").strip() or "کاربر"
        coins = await db.select('wallet', ['coins'], {'userID': str(userID)})
        coins = coins[0]['coins'] if coins else 0
        line = f"""🆔: `{user['userID']}`
        نام: {name}
       نام کاربری: @{default_name.username if default_name and default_name.username else f'[{name}](tg://user?id={userID})'}
        موجودی: {coins} تومان
        شغل: {user['work'] or 'تعریف نشده'}
        وضعیت حرکت: {user['move'] or 'تعریف نشده'}
        کارت بانکی: {user['card'] or 'تعریف نشده'}"""

        message_lines.append(line)
    
    await db.update('users', {'move': None}, {'userID': m.chat.id})
    await m.reply("\n".join(message_lines))