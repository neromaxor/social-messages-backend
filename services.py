from telethon.sync import TelegramClient

API_ID = 'your_api_id'  # Технічний параметр, який треба отримати у Telegram
API_HASH = 'your_api_hash'

def get_telegram_chats(telegram_id: str):
    try:
        with TelegramClient(telegram_id, API_ID, API_HASH) as client:
            dialogs = client.get_dialogs(limit=10)  # Отримати діалоги
            return [{"chat_name": dialog.name, "chat_id": dialog.id} for dialog in dialogs]
    except Exception as e:
        raise Exception(f"Error retrieving chats: {str(e)}")
