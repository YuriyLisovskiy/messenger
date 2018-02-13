import smtplib
from email.mime.text import MIMEText

from django.http import JsonResponse

from account.models import UserProfile
from utils.helpers import email_does_not_exist
from utils.responses import CREATED, BAD_REQUEST
from messenger.settings import EMAIL_HOST, EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_PORT


def send_email(request):
	if request.method == 'POST':
		if 'generated_code' in request.POST and 'user_email' in request.POST:
			usr_email = request.POST.get('user_email')
			if not email_does_not_exist(usr_email, UserProfile.get_all()):
				response = {
					'error': 'User with this email already exists',
					'status': 'BAD'
				}
				return JsonResponse(response, status=400, safe=False)
			generated_code = request.POST.get('generated_code')
			request.session['gen_code'] = generated_code
			message_content = """This is data for signing in Your account:
 Login:           {}\n Password:    {}\n
Do not show this message to anyone to prevent stealing your account!
The last step you should perform is to enter this code: "{}".\n
Thank You for registering on our website.
Best regards, messenger support.""".format(
				request.POST.get('username'),
				request.POST.get('password'),
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
			return CREATED
	return BAD_REQUEST
