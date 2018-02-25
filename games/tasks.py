from background_task import background
from django.core.mail import send_mail

@background(schedule=60)
def email(subject, body, from_email, to_email):

    send_mail(subject, body, from_email, [to_email], fail_silently=True)
