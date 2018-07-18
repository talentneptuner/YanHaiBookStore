from users.models import EmailCode
from random import Random

from django.core.mail import send_mail
from YanHai.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str = str + chars[(random.randint(0, length))]
    return str

def send_email(email,type):
    emailcode = EmailCode()
    emailcode.email = email
    emailcode.send_type = type
    emailcode.code = random_str(5)
    emailcode.save()

    email_title = "您的验证码是"
    email_body = emailcode.code
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
