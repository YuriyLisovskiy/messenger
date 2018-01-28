import smtplib
from email.mime.text import MIMEText

from datetime import datetime
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import redirect

from utils.helpers import email_does_not_exist
from messenger.settings import *
from utils.responses import NOT_FOUND, BAD_REQUEST
from chat.models import Message, ChatRoom
from utils.view_modifiers import auth_required
from account.models import UserProfile


class ChatManager(View):
	
	@auth_required
	def get(self, request):
		if 'msgs_amount' in request.GET and 'chat_room_data' in request.GET:
			data = {
				'author': UserProfile.get_by_id(request.user.id),
				'friend': UserProfile.get_by_id(request.GET.get('chat_room_data'))
			}
			chat_room = ChatRoom.filter_by(**data)
			if chat_room:
				data = {
					'chat_room': chat_room.first()
				}
				messages = Message.filter_by(**data)
				msgs_amount = len(messages)
				response_data = {
					'amount': msgs_amount
				}
				return JsonResponse(response_data)
		if 'chat_room_data' in request.GET:
			filter_data = {
				'author': UserProfile.get_by_id(request.user.id),
				'friend': UserProfile.get_by_id(request.GET.get('chat_room_data'))
			}
			chat_room = ChatRoom.filter_by(**filter_data)
			if not chat_room:
				return NOT_FOUND()
			filter_data = {
				'chat_room': chat_room.first()
			}
			messages = Message.filter_by(**filter_data)
			response = {
				'data': [message.to_dict() for message in messages],
				'status': 'OK'
			}
			return JsonResponse(response, safe=False)
		return BAD_REQUEST()
	
	@auth_required
	def post(self, request):
		msg = request.POST.get('msg')
		if msg != '':
			msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + str(
				datetime.now().strftime("%d %b %Y"))[:11]
			author = UserProfile.get_by_id(request.user.id)
			friend = UserProfile.get_by_id(request.POST.get('friend_id'))
			if not author and not friend:
				return NOT_FOUND()
			filter_data = {
				'author': author,
				'friend': friend
			}
			chat_room = ChatRoom.filter_by(**filter_data)
			if not chat_room:
				room_data = {
					'author': author,
					'friend': friend,
					'logo': friend.user_logo
				}
				chat_room = ChatRoom.add(**room_data)
			message_data = {
				'chat_room': chat_room.first(),
				'author': author,
				'msg': msg,
				'time': msg_time,
			}
			Message.add(**message_data)
			if author != friend:
				filter_data = {
					'author': friend,
					'friend': author
				}
				chat_room = ChatRoom.filter_by(**filter_data)
				if not chat_room:
					room_data = {
						'author': friend,
						'friend': author,
						'logo': author.user_logo
					}
					chat_room = ChatRoom.add(**room_data)
				message_data = {
					'chat_room': chat_room.first(),
					'author': author,
					'msg': msg,
					'time': msg_time,
				}
				Message.add(**message_data)
			return JsonResponse({'status_message': 'Message has been sent!'})
		return JsonResponse({'status_message': 'Message is empty!'})
	
	@auth_required
	def delete(self, request):
		data = {
			'author': UserProfile.get_by_id(request.user.id),
			'friend': UserProfile.get_by_id(request.POST.get('delete_chat_room'))
		}
		chat_room = ChatRoom.filter_by(**data)
		if chat_room:
			chat_room.first().delete()
			response = {
				'success': 'Chat room has been deleted.'
			}
			return JsonResponse(response)
		else:
			return NOT_FOUND()


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
