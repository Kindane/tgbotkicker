import asyncio
import logging
from database import chats
from aiogram.types.update import AllowedUpdates
from aiogram import exceptions
from aiogram import Bot, types
from settings import TOKEN, ADMINS

bot = Bot(token=TOKEN)


logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")
Bot.set_current(bot)


async def get_updates():
    offset = None
    while True:
        updates = await bot.get_updates(offset=offset, timeout=20, allowed_updates=AllowedUpdates.MY_CHAT_MEMBER+AllowedUpdates.MESSAGE)
        for update in updates:
            offset = update.update_id.real + 1
            print(update)
            if update.my_chat_member: # someone added me to group
                chatID = update.my_chat_member.chat.id
                if chatID not in chats:
                    chats.add_chat(chatID)
            else: # someone send me message
                message = update.message
                if message.from_user.id not in ADMINS: # ignore every user but not admins
                    continue
                text = message.text
                if message.is_command():
                    if text.startswith("/ban") and len(text.split()) == 2: # /ban 1234
                        user_to_kick = update.message.text.split()[-1]
                        if not user_to_kick.isdigit():
                            await message.answer("You should call 'ban' command with argument like @username")
                            continue
                        for chat in chats:
                            chat = await bot.get_chat(chat)
                            try:
                                await chat.kick(int(user_to_kick))
                            except Exception as e:
                                if not "supergroup" in str(e):
                                    await message.answer(f"Something went wrong in chat {chat.title}\nException: {e}")
                                    continue
                    else:
                        await message.answer("You should write '/ban userID' to ban someone and be admin")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(get_updates())
    loop.run_forever()