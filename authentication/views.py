import smtplib
from email.mime.text import MIMEText

from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import login
from django.http import JsonResponse
from django.views import View

from account.models import UserProfile
from messenger.settings import EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT
from utils.helpers import email_does_not_exist
from utils.responses import BAD_REQUEST, CREATED, OK, NOT_FOUND


class SignUp(View):

	def get(self, request):
		return BAD_REQUEST

	def post(self, request):
		form = request.POST
		for key in ['first_name', 'last_name', 'email', 'password', 'code']:
			if key not in form.keys():
				break
		else:
			first_name = form.get('first_name')
			last_name = form.get('last_name')
			password = form.get('password')
			email = form.get('email')
			generated_code = form.get('code')
			errors = {}
			if not email_does_not_exist(email, UserProfile.objects.all()):
				errors['email'] = 'account with this email address already exists'
			if generated_code != request.session['gen_code']:
				errors['code'] = 'incorrect received code'
			if len(errors) > 0:
				response = {
					'data': {
						'errors': errors
					},
					'status': 'BAD'
				}
				return JsonResponse(response, status=400, safe=False)
			else:
				data = {
					'first_name': first_name,
					'last_name': last_name,
					'email': email,
					'password': password
				}
				profile = UserProfile.add(**data)
				user = authenticate(username=profile.username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						return CREATED
		return BAD_REQUEST


class SignIn(View):

	def get(self, request):
		return BAD_REQUEST

	def post(self, request):
		if request.user.is_authenticated:
			return JsonResponse({
				'authenticated': True,
				'status': "SUCCESS"
			})
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username and password:
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return OK
				else:
					response = {
						'data': {
							'error': 'Your account has been disabled'
						},
						'status': 'BAD'
					}
			else:
				response = {
					'data': {
						'error': 'Invalid login or password'
					},
					'status': 'BAD'
				}
			return JsonResponse(response, status=400, safe=False)
		return BAD_REQUEST


class SignOut(View):

	def get(self, request):
		logout(request)
		return CREATED

	def post(self, request):
		return BAD_REQUEST


class CheckEmail(View):

	def get(self, request):
		if 'email' in request.GET:
			user = UserProfile.filter_by(email=request.GET.get('email'))
			if user:
				return OK
			else:
				return NOT_FOUND
		else:
			return BAD_REQUEST

	def post(self, request):
		return BAD_REQUEST


class SendEmail(View):

	def get(self, request):
		return BAD_REQUEST

	def post(self, request):
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
