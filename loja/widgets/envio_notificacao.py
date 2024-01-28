from django.core.mail import send_mail
from django.template.loader import render_to_string
from gbstr import settings
from twilio.rest import Client

def enviar_email(destinatario, assunto, template, contexto):
    mensagem = render_to_string(template, contexto)
    send_mail(assunto, mensagem, settings.EMAIL_HOST_USER, [destinatario])

def enviar_whatsapp(destinatario, mensagem):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=mensagem,
        from_='whatsapp:' + twilio_phone_number,
        to='whatsapp:' + destinatario
    )

    return message.sid