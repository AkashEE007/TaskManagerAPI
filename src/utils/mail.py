import os

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr, NameEmail, SecretStr


class EmailSchema(BaseModel):
    email: list[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "akashshetty508@gmail.com",
    MAIL_PASSWORD="vtvn qmva mtji gwyb",
    MAIL_FROM = "akashshetty508@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="FastAPI automated API",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(emails: list[str], subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[NameEmail(name=email, email=email) for email in emails],
        body=body,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

