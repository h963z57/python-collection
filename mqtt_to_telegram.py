import paho.mqtt.client as mqtt
from telegram import Bot
import asyncio

# MQTT settings
mqtt_info = "wb/info"
mqtt_warning = "wb/warning"
mqtt_critical = "wb/critical"

# TG settings
TOKEN = '{{ token }}'
CHAT_ID = ''

# MQTT Callback
def on_message(client, userdata, message):
    topic = message.topic
    value = message.payload.decode()

    if mqtt_info:
        asyncio.run(main(TOKEN, CHAT_ID, value))

async def main(TOKEN, CHAT_ID, MESSAGE):
    bot_token = TOKEN
    chat_id = CHAT_ID
    # message = "{{ role }} - " + MESSAGE
    message = MESSAGE

    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

# MQTT Setup
client = mqtt.Client(userdata={})
client.on_message = on_message
client.connect("127.0.0.1")
client.subscribe(mqtt_info)
client.subscribe(mqtt_warning)
client.subscribe(mqtt_critical)

client.loop_forever()