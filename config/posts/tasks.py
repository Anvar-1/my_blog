from celery import shared_task
import requests

@shared_task
def send_telegram_message_task(name, message):
    token = "7512345678:AAH_O'Z_TOKENINGIZ"
    chat_id = "123456789"
    text = f"📩 *Yangi xabar!*\n\n👤 *Kimdan:* {name}\n📝 *Xabar:* {message}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})