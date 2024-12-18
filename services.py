from telethon import TelegramClient
import logging

logging.basicConfig(level=logging.DEBUG)

# Telegram authorization client
async def get_telegram_client(session_name: str, api_id: str, api_hash: str):
    client = TelegramClient(session_name, api_id, api_hash)
    return client

async def start_telegram_session(client: TelegramClient, phone: str):
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
        return client
    except Exception as e:
        logging.error(f"Error during Telegram session start: {e}")
        return None

async def get_telegram_chats(client: TelegramClient):
    try:
        dialogs = await client.get_dialogs()
        chats = []
        for dialog in dialogs:
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

        return chats
    except Exception as e:
        logging.error(f"Error fetching chats: {e}")
        return []
#services.py