import smtplib
from email.mime.text import MIMEText

from django.http import JsonResponse
from django.shortcuts import redirect

from messenger.settings import *
from account.models import UserProfile
from utils.helpers import email_does_not_exist


def send_email(request):
	if request.user.is_authenticated:
		return redirect('index')
	if 'generated_code' in request.GET and 'user_email' in request.GET:
		usr_email = request.GET.get('user_email')
		if not email_does_not_exist(usr_email, UserProfile.get_all()):
			return JsonResponse({
				'error_code': "222",
				'name': "User with this email address already exists!"
			})
		generated_code = request.GET.get('generated_code')
		request.session['gen_code'] = generated_code
		message_content = """This is data for signing in Your account:
 Login:           {}\n Password:    {}\n
Do not show this message to anyone to prevent stealing your account!
The last step you should perform is to enter this code: "{}".\n
Thank You for registering on our website.
Best regards, messenger support.""".format(
			request.GET.get('username'),
			request.GET.get('password'),
			generated_code
		)
		support_email = "mymessengerhelp@gmail.com"
		message_subject = 'Messenger sign up'
		message = MIMEText(message_content)
		message['Subject'] = message_subject
		message['From'] = support_email
		message['To'] = usr_email
		new_email = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
		new_email.ehlo()
		new_email.starttls()
		new_email.ehlo()
		new_email.login(EMAIL_LOGIN, EMAIL_PASSWORD)
		new_email.sendmail(support_email, [usr_email], message.as_string())
		new_email.quit()
		return JsonResponse({'name': "Code was sent successfully!"})
	return JsonResponse({
		'error_code': "222",
		'name': "Error occurred while sending email!"
	})
