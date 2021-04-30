import os
from telethon import TelegramClient, events
import time
import math
import re
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters

# Initializing telethon parameters
t_api_id = os.environ['t_api_id']
t_api_hash = os.environ['t_api_hash']
channel_id = os.environ['channel_id']
channel_link = os.environ['channel_link']

# Updating keywords
def update_list():
  my_file = open("keywords.txt", "r")
  content = my_file.read()
  new_keywords_list = content.split(",")
  my_file.close()
  return new_keywords_list
  
keywords_list=update_list()


# Initializing telegram-bot parameters
tok = os.environ['token']

updater = Updater(token=tok, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

chat_bot=""
adding=False  # True when user wants to add keyword to the list
removing=False # True when user wants to remove keyword from the list

def start(update, context):
	global chat_bot
	chat = update.effective_chat.id
	chat_bot=chat
	context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Notification Bot. Send /add to add a new keyword. Send /list to show all the saved keywords.")

# Send list of keywords
def list_fun(update,context):
  chat = update.effective_chat.id
  text_list="Keywords:\n"
  for keyword in keywords_list:
    text_list=text_list+"- "+keyword+"\n"
    
  context.bot.send_message(chat_id=update.effective_chat.id, text=text_list)

# Ask for new keyword
def add(update,context):
  global adding
  chat = update.effective_chat.id
  context.bot.send_message(chat_id=update.effective_chat.id, text="Which keyword you wish to add to the list?")
  adding=True

# Add new keyword to list file
def keyword_add(update,context):
  global keywords_list
  global adding
  global removing
  chat = update.effective_chat.id
    
  if adding==True:
    keyword=update.message.text
    my_file = open("keywords.txt", "a+")
    my_file.write(","+keyword)
    my_file.close()
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Added "+keyword+" to the list")
    
    adding=False
    
    keywords_list=update_list() # update actual list
  
  elif removing==True:
    keyword=update.message.text
    if keyword in keywords_list:
      keywords_list.remove(keyword) #removing keyword from the list
      # generating new keywords text
      print(keywords_list)
      n=len(keywords_list)
      text_list=""
      for i in range(0,n):
        if i<n-1:
          text_list=text_list+keywords_list[i]+","
        else:
          text_list=text_list+keywords_list[i]
          
      my_file = open("keywords.txt", "w+")
      my_file.write(text_list)
      my_file.close()
      
      removing=False
      keywords_list=update_list() # update actual list
        
      context.bot.send_message(chat_id=update.effective_chat.id, text="Removed "+keyword+" from the list")
      
    else:
      context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I can't find"+keyword+" in the list. Try again")
      
      
        
        
# Ask the keyword to remove
def remove(update,context):
  global removing
  chat = update.effective_chat.id
  context.bot.send_message(chat_id=update.effective_chat.id, text="Which keyword you wish to remove frome the list?")
  removing=True


start_handler = CommandHandler('start', start)
list_handler = CommandHandler('list', list_fun)
add_handler = CommandHandler('add', add)
remove_handler = CommandHandler('remove', remove)
key_handler=MessageHandler(Filters.text, keyword_add)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(remove_handler)
dispatcher.add_handler(key_handler)

updater.start_polling()


t_client = TelegramClient('anon', t_api_id, t_api_hash)
# Start searching for keywords
@t_client.on(events.NewMessage)
async def my_event_handler(event):
  if event.chat.id != chat_bot: # Check if the message comes from the chat with bot itself
    for keyword in keywords_list:
    	match = re.search(keyword, event.raw_text)
    	if match:
        # Bot send alert to channel
    		updater.bot.send_message(chat_id=int(channel_id), text="Found keyword!")
    		channel = await t_client.get_entity(channel_link)
    		
    		# Telethon forwards the message
    		await t_client.forward_messages(channel, event.message)

t_client.start()
t_client.run_until_disconnected()
