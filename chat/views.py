import smtplib
from email.mime.text import MIMEText

from datetime import datetime
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect

from utils.helpers import email_does_not_exist
from messenger.settings import *
from account.models import UserProfile
from .models import Message, ChatRoom
from utils.responses import NOT_FOUND, BAD_REQUEST
from utils.view_modifiers import auth_required
from .serializers import MessageSerializer, UserSerializer


def index(request):
	return render(request, "chat/index.html")


@auth_required
def chat(request):
	user = request.user
	all_users = UserProfile.get_all()
	all_chat_rooms = ChatRoom.get_all()
	return render(request, "chat/chat.html", {
		'user': user,
		'all_users': all_users,
		'all_chat_rooms': all_chat_rooms
	})


class SearchPeople(View):

	@auth_required
	def get(self, request):
		data = UserProfile.get_all()
		return render(request, "chat/search.html", {'all_users': data})

	@auth_required
	def post(self, request):
		keyword = request.POST.get('search')
		if 'city' in request.POST:
			f_n, l_n = keyword.split()
			filter_data = {
				'first_name': f_n,
				'last_name': l_n,
				'city': request.POST.get('city'),
				'country': request.POST.get('country'),
				'birthday': request.POST.get('birthday'),
				'gender': request.POST.get('gender')
			}
			data = UserProfile.filter_by(**filter_data)
		elif " " in keyword:
			f_n, l_n = keyword.split()
			filter_data = {
				'first_name__icontains': f_n,
				'last_name__icontains': l_n
			}
			data = UserProfile.filter_by(**filter_data)
		else:
			first_name_data = {
				'first_name__icontains': keyword
			}
			last_name_data = {
				'last_name__icontains': keyword
			}
			data = UserProfile.filter_by(**first_name_data) | UserProfile.filter_by(**last_name_data)
		serializer = UserSerializer(data, many=True)
		return JsonResponse(serializer.data, safe=False)


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
			serializer = MessageSerializer(messages, many=True)
			return JsonResponse(serializer.data, safe=False)
		return BAD_REQUEST()

	@auth_required
	def post(self, request):
		msg = request.POST.get('msg')
		if msg != '':
			msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + str(datetime.now().strftime("%d %b %Y"))[:11]
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
			return JsonResponse({'success': 'Chat room has been deleted.'})
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
