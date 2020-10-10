from telegram.ext import CommandHandler, run_async, MessageHandler
from telegram.ext.filters import Filters
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from time import sleep

@run_async
def start(update,context):
    sendMessage(f'Hi, I can search for files in my Google Drive Database and returns a list of matching files with Google Drive Link.\n- Just send me the File Name.\n\nI am also usable in Groups just add me in any Group and send\n/search File Name.', context.bot, update)

@run_async
def delete(update,context):
  msg = sendMessage('Deleting...',context.bot,update)
  gdrive = GoogleDriveHelper(None)
  text = gdrive.deleteFile(update.message.text)
  editMessage(text,msg)
  deleteMessage(context.bot,update.message)
  sleep(6)
  deleteMessage(context.bot,msg)


@run_async
def list_drive(update,context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        reply = sendMessage(f'Searching for {search} in my Google Drive Database...', context.bot, update)

        LOGGER.info(f"Searching: {search}")
        
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        editMessage(msg,reply,button)

    except IndexError:
        sendMessage('send a search key along with command', context.bot, update)

@run_async
def msg_list_drive(update,context):
    try:
        search = update.message.text
        reply = sendMessage(f'Searching for {search} in my Google Drive Database...', context.bot, update)

        LOGGER.info(f"Searching: {search}")
        
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        editMessage(msg,reply,button)

    except IndexError:
        sendMessage('send a search key along with command', context.bot, update)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive)
msg_handler = MessageHandler(Filters.private & (~ Filters.command), msg_list_drive)
start_msg = CommandHandler(BotCommands.StartCommand, start)
del_handler = CommandHandler(command=BotCommands.DelCommand, callback=delete, filters=CustomFilters.owner_filter & Filters.group)
dispatcher.add_handler(msg_handler)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(start_msg)
dispatcher.add_handler(del_handler)