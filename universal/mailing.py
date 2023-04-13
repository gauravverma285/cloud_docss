from threading import Thread
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from queue import *

mail_from = settings.EMAIL_HOST_USER


concurrent = 50
que = Queue(concurrent*10)

def DataProcess():
	while True:
		params = que.get()
		subject = params['subject']
		message = params['message']
		recipient_list = params['recipient_list']
		send_mail(subject, message, mail_from, recipient_list, fail_silently=False)
		
		que.task_done()

for i in range(concurrent):
	t = Thread(target=DataProcess)
	t.daemon = True
	t.start()

def EmailThreading(subject, message, recipient_list):
	param = {'subject': subject, 'message':message, 'recipient_list':recipient_list}
	que.put(param)

que.join()


def signupMail(subject, recipient_list, name, otp):
	html_content = render_to_string('mail/signup_mail.html', {'name':name, 'otp':otp})
	# print(html_content)
	text_content = strip_tags(html_content) 

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, mail_from, recipient_list)
	msg.attach_alternative(html_content, "text/html")
	print(msg)
	msg.send()

def resetPassMail(subject, recipient_list, name, otp):
	html_content = render_to_string('mail/forgot_password_mail.html', {'name':name, 'otp':otp})
	text_content = strip_tags(html_content) 

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, mail_from, recipient_list)
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	
def resendOtpMail(subject, recipient_list, name, otp):
	html_content = render_to_string('mail/resend_otp_mail.html', {'name':name, 'otp':otp})
	text_content = strip_tags(html_content) 

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, mail_from, recipient_list)
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def verifyEMail(subject, recipient_list, name, otp):
	html_content = render_to_string('mail/verify_email_mail.html', {'name':name, 'otp':otp})
	text_content = strip_tags(html_content) 

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, mail_from, recipient_list)
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def successSignupMail(subject, recipient_list, name):
	html_content = render_to_string('mail/signup_success_mail.html', {'name':name})
	text_content = strip_tags(html_content) 

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, mail_from, recipient_list)
	msg.attach_alternative(html_content, "text/html")
	msg.send()