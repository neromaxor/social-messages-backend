from telethon import TelegramClient
import logging
import asyncio

# Налаштування для логування
logging.basicConfig(level=logging.DEBUG)

# Ваші налаштування API
api_id = '23023743'  # Замініть на ваше API ID
api_hash = '26eb73659882b22b4f8c6bea8a61a951'  # Замініть на ваш API HASH
api_number = '+380635939802'  # Ваш номер телефону в міжнародному форматі

# Створення клієнта
client = TelegramClient('session_name', api_id, api_hash)

# Функція для отримання чатів
async def get_telegram_chats(telegram_id: str):
    try:
        # Підключення до Telegram за номером телефону
        await client.start(api_number)

        # Отримання всіх чатів
        dialogs = await client.get_dialogs()
        chats = []
        for dialog in dialogs:
            # Перевірка типу діалогу
            if dialog.is_group:
                chat_type = "group"
            elif dialog.is_channel:
                chat_type = "channel"
            else:
                chat_type = "private"

            chats.append({
                "chat_id": dialog.id,
                "chat_name": dialog.name,
                "chat_type": chat_type
            })

        await client.disconnect()

        # Повертаємо список чатів
        return chats

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await client.disconnect()


#services.py