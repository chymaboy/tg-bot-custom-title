import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from cities import CITIES


TEST_GROUP = -1001505395927


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f'user: {update.message.from_user.username}, message: {update.message.text}')
    await update.message.reply_text("Чтобы установить город напиши /city НАЗВАНИЕ_ГОРОДА")
    await update.message.reply_text("Чтобы очистить статус напиши /clear")
    await update.message.reply_text("Чтобы получить помощь напиши /help")


async def clear_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f'user: {update.message.from_user.username}, message: {update.message.text}')
    chat_id = TEST_GROUP
    user_id = update.message.from_user.id
    await context.bot.promoteChatMember(chat_id, user_id,
                                        is_anonymous=False,
                                        can_manage_chat=False,
                                        can_delete_messages=False,
                                        can_restrict_members=False,
                                        can_promote_members=False,
                                        can_pin_messages=False,
                                        can_manage_video_chats=False,
                                        can_invite_users=False,
                                        )
    await update.message.reply_text("Статус очищен")


async def update_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f'user: {update.message.from_user.username}, message: {update.message.text}')
    input_message = update.message.text.split()
    if len(input_message) == 1:
        await update.message.reply_text("Вы не ввели название города")
        return
    elif len(input_message) > 2:
        await update.message.reply_text("Вы ввели больше одного слова после команды /city")
        return
    city = input_message[1]
    chat_id = TEST_GROUP
    user_id = update.message.from_user.id
    if city in CITIES:
        await context.bot.promoteChatMember(chat_id, user_id,
                                            is_anonymous=False,
                                            can_manage_chat=False,
                                            can_delete_messages=False,
                                            can_restrict_members=False,
                                            can_promote_members=False,
                                            can_pin_messages=True,
                                            can_manage_video_chats=True,
                                            can_invite_users=True,
                                            )
        await context.bot.setChatAdministratorCustomTitle(chat_id, user_id, city)
        await update.message.reply_text("Город обновлён")
    else:
        await update.message.reply_text("Такого города нет. Проверьте написание в списке "
                                        "https://ru.wikipedia.org/wiki/Список_населённых_пунктов_Турции")


if __name__ == '__main__':
    app = ApplicationBuilder().token("5392460763:AAHsxAZWbll5LIe5v3KXUWtwl4BIPmJ0GNw").build()
    app.add_handler(CommandHandler("city", update_city))
    app.add_handler(CommandHandler("clear", clear_status))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.run_polling()
