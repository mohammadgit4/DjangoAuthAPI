from django.core.mail import send_mail
from django.conf import settings

class Util:
    def send_link(data):
        send_mail(data['subject'], data['message'], settings.EMAIL_HOST, data['to_email'])