import asyncio
import telegram
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import paho.mqtt.publish as publish
# import os

MQTT_BROKER = '127.0.0.1'
MQTT_TOPIC = 'wb/from_telegram'
TELEGRAM_TOKEN = '{{ token }}'
ROLE = '{{ role }}'
CHAT_ID = ''

async def main():
    bot = telegram.Bot(TELEGRAM_TOKEN)
    offset = None  # Initialize offset

    while True:
        async with bot:
            updates = await bot.get_updates(offset=offset, timeout=10)
            if updates:
                for update in updates:
                    # Update the offset to the latest update_id + 1
                    offset = update.update_id + 1
                    if update.message:
                        # Process new messages here
                        print(update.message.text)
                        if update.message.text == "status":
                            publish.single("wb/warning", "telegram system is working", hostname=MQTT_BROKER)
                        
                        
                        if update.message.text == "/start":
                            # keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Кнопка", callback_data='data')]])
                            keyboard = ReplyKeyboardMarkup([
                                [KeyboardButton("Поставить на охрану"), KeyboardButton("Снять с охраны")],
                                [KeyboardButton("status")]
                            ], resize_keyboard=True, one_time_keyboard=True)
                            bot = Bot(token=TELEGRAM_TOKEN)
                            await bot.send_message(chat_id=CHAT_ID, text='Выберите действие', reply_markup=keyboard)
                        else:
                            publish.single(MQTT_TOPIC, update.message.text, hostname=MQTT_BROKER)
            await asyncio.sleep(1)  # Short delay to avoid busy loop

if __name__ == '__main__':
    asyncio.run(main())