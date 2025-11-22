from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import logging

app = FastAPI(title="Сервис отправки уведолмений на почту", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationRequest(BaseModel):
    to_email: str
    subject: str
    message: str
    user_name: str = "User"


class NotificationResponse(BaseModel):
    status: str
    message_id: str
    timestamp: str


@app.get("/")
def read_root():
    return {"message": "Сервис отправки уведомлений на почту запущен!"}


@app.post("/send-notification/", response_model=NotificationResponse)
def send_notification(notification: NotificationRequest):
    """Имитация отправки email уведомления"""

    message_id = f"msg_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    logger.info(f"""
    📧 EMAIL УВЕДОМЛЕНИЕ ОТПРАВЛЕНО:
    Кома: {notification.to_email}
    Тема: {notification.subject}
    Сообщение: {notification.message}
    Сообщение ID: {message_id}
    Дата отправления: {datetime.now()}
    """)

    return NotificationResponse(
        status="отправлено",
        message_id=message_id,
        timestamp=datetime.now().isoformat()
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)