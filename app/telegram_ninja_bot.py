from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import telegram
from post_crudl import create_post, list_of_posts
from user_crudl import telegram_registration_final
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Словарь для конв хэндлера
TITLE, DESCRIPTION, PUBLIC = range(3)

# Словарь для Названия и Описания поста
post_values = {'title': 0, 'description': 0}


# Связка телеграм айди с аккаунтом на сайте
def registration(bot, update, args):
    chat_id = update.message.chat_id
    reg = telegram_registration_final(args[0], chat_id)
    if reg:
        bot.sendMessage(chat_id=chat_id, text='Registration success')
    else:
        bot.sendMessage(chat_id=chat_id, text='Registration failed')


# Обработка ошибок
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


# Конв хэндлер. Начало создания поста
def add_post(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text='Start new post')
    bot.sendMessage(chat_id=chat_id, text='*Please, enter the title*', parse_mode=telegram.ParseMode.MARKDOWN)
    return TITLE


# Конв хэндлер. Создаём название поста
def add_title(bot, update):
    chat_id = update.message.chat_id
    title = update.message.text
    post_values['title'] = title
    bot.sendMessage(chat_id=chat_id, text='*Please, enter the description*', parse_mode=telegram.ParseMode.MARKDOWN)
    return DESCRIPTION


# Конв хэндлер. Создаём описание
def add_description(bot, update):
    chat_id = update.message.chat_id
    description = update.message.text
    post_values['description'] = description
    post_text = '*{}* \n {} \n \n If you want to create post, please send /create, \n ' \
                'else send /cancel'.format(post_values['title'], post_values['description'])
    bot.sendMessage(chat_id=chat_id, text=post_text, parse_mode=telegram.ParseMode.MARKDOWN)
    return PUBLIC


# Конв хэндлер. Создаём новый пост
def create_new_post(bot, update):
    chat_id = update.message.chat_id
    post = create_post(chat_id, post_values['title'], post_values['description'])
    if post:
        bot.sendMessage(chat_id=chat_id, text='*Post created*', parse_mode=telegram.ParseMode.MARKDOWN)
        post_values.clear()
    else:
        bot.sendMessage(chat_id=chat_id, text='*Unknown user*', parse_mode=telegram.ParseMode.MARKDOWN)
    return ConversationHandler.END


# Конв хэндлер. Отменям конв хэндлер.
def cancel(bot, update):
    print('Stop')
    return ConversationHandler.END

def list_posts(bot, update):
    result = ''
    chat_id = update.message.chat_id
    list = list_of_posts(chat_id)
    for i in range(len(list)):
        message = '/{}\n'.format(list[i].title)
        result += message
    bot.sendMessage(chat_id=chat_id, text=result)



def main():

    updater = Updater('133728555:AAE8ql64wXK9IcnLXTm9YMEP38REaemfvg8')
    dp = updater.dispatcher

    conv_handler = ConversationHandler(entry_points=[CommandHandler('new', add_post)],
                                       states={
                                           TITLE: [MessageHandler(Filters.text, add_title)],
                                           DESCRIPTION: [MessageHandler(Filters.text, add_description)],
                                           PUBLIC: [CommandHandler('create', create_new_post)]
                                       },
                                       fallbacks=[CommandHandler('cancel', cancel)])
    dp.add_handler(CommandHandler('start', registration, pass_args=True))
    dp.add_handler(CommandHandler('list', list_posts))
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
