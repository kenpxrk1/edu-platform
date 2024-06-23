from email.message import EmailMessage
import smtplib
from celery import Celery
from pydantic import EmailStr
from app.core.config import email_config



celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def send_verify_token(email: EmailStr, token):
    msg = EmailMessage()
    msg["Subject"] = "Подтвердите электронную почту"
    msg["From"] = email_config.SECRET_EMAIL
    msg["To"] = email

    msg.set_content(
        f""" 

    <h1>Подтверждение электронного адреса на сайте Планета Курсов</h1>

    <p><br>Здравствуйте!</br></p> 

   <p> Вы получили это письмо, потому что зарегистрировались на нашем сайте. Пожалуйста, подтвердите свою электронную почту, перейдя по следующей ссылке:

    http://127.0.0.1:8000/users/verify?token={token}</p>

    <p>Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.<p>

    <p>Спасибо!
    С уважением,
    Команда Планеты Курсов</p>

         """,
        subtype="html",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_config.APP_EMAIL, email_config.SECRET_EMAIL)
        smtp.send_message(msg)