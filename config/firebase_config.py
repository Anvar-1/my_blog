import firebase_admin
from firebase_admin import credentials, messaging

# JSON faylga yo'l
cred = credentials.Certificate("path/to/your-service-account-file.json")
firebase_admin.initialize_app(cred)

def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    response = messaging.send(message)
    print('Xabar yuborildi:', response)