from telethon import TelegramClient, events
import time
import math
import re 

t_api_id = 3882522
t_api_hash = 'b4ba5e7ea1e710aa74c9b2fb1c29ea98'
t_client = TelegramClient('anon', t_api_id, t_api_hash)

@t_client.on(events.NewMessage)
async def my_event_handler(event):
        match=re.search('[#$]([a-zA-Z]*)',event.raw_text)
        if match:
             coin=match.group(1)
             await client.forward_messages("-1001483829428",event.message)
)

t_client.start()
t_client.run_until_disconnected()



