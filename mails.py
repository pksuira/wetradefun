from google.appengine.api import mail

from django.http import HttpResponse

def send(subject, from_name, from_email, to_name, to_email, body):
  message = mail.EmailMessage(sender=from_name + " <"+from_email+">",
    subject=subject)

  message.to = to_name + " <"+to_email+">"
  message.body = body

  message.send # comment this line if testing on local machine 