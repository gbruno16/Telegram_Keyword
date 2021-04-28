import os
from telethon import TelegramClient, events
import time
import math
import re 
from telegram.ext import Updater
import logging

t_api_id= os.environ['t_api_id']
t_api_hash= os.environ['t_api_hash']
channel_id=os.environ['channel_id']
channel_link=os.environ['channel_link']

tok=os.environ['token']

updater = Updater(token=tok, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    
    chat=update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id, text=chat)                  
    
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
t_client = TelegramClient('anon', t_api_id, t_api_hash)

@t_client.on(events.NewMessage)
async def my_event_handler(event):
        match=re.search('##',event.raw_text)
        if match:
            
             updater.bot.send_message(chat_id=int(channel_id),text="Canale")
             channel= await t_client.get_entity(channel_link)
             await t_client.forward_messages(channel,event.message)


t_client.start()
t_client.run_until_disconnected()



