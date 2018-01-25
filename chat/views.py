import smtplib
from email.mime.text import MIMEText

from datetime import datetime
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from utils import functions
from messenger.settings import *
from account.models import UserProfile
from .models import Message, ChatRoom
from utils.responses import NOT_FOUND
from utils.view_modifiers import auth_required
from .serializers import MessageSerializer, UserSerializer


def index(request):
	return render(request, "chat/index.html")


@auth_required
def chat(request):
	user = request.user
	all_users = UserProfile.objects.all()
	all_chat_rooms = ChatRoom.objects.all()
	return render(request, "chat/chat.html", {
		'user': user,
		'all_users': all_users,
		'all_chat_rooms': all_chat_rooms
	})


class SearchPeople(View):

	@auth_required
	def get(self, request):
		data = UserProfile.objects.all()
		return render(request, "chat/search.html", {'all_users': data})

	@auth_required
	def post(self, request):
		keyword = request.POST['search']
		if 'city' in request.POST:
			f_n, l_n = keyword.split()
			birthday = request.POST['birthday']
			data = UserProfile.objects.filter(
				first_name=f_n,
				last_name=l_n,
				user_city=request.POST['city'],
				user_country=request.POST['country'],
				user_birthday_day=birthday[8:],
				user_birthday_month=birthday[5:7],
				user_birthday_year=birthday[:4],
				user_gender=request.POST['gender']
			)
		elif " " in keyword:
			f_n, l_n = keyword.split()
			data = UserProfile.objects.filter(
				first_name__icontains=f_n,
				last_name__icontains=l_n
			)
		else:
			data = UserProfile.objects.filter(first_name__icontains=keyword) | UserProfile.objects.filter(
				last_name__icontains=keyword)
		serializer = UserSerializer(data, many=True)
		return JsonResponse(serializer.data, safe=False)


class ChatManager(View):

	@auth_required
	def delete(self, request):
		friend_id = request.POST['delete_chat_room']
		try:
			ChatRoom.objects.get(author__id=request.user.id, friend__id=friend_id).delete()
		except ChatRoom.DoesNotExist:
			return NOT_FOUND()
		return JsonResponse({'success': 'Chat room has been deleted.'})

	@auth_required
	def get(self, request):
		if 'msgs_amount' in request.GET and 'chat_room_data' in request.GET:
			msgs_am = len(Message.objects.filter(
				chat_room=ChatRoom.objects.get(
					friend__id=request.GET['chat_room_data'],
					author__id=request.user.id
				))
			)
			response_data = {'amount': msgs_am}
			return JsonResponse(response_data)
		if 'chat_room_data' in request.GET:
			chat_room_msgs = Message.objects.filter(
				chat_room=ChatRoom.objects.get(
					friend__id=request.GET['chat_room_data'],
					author__id=request.user.id
				)
			)
			serializer = MessageSerializer(chat_room_msgs, many=True)
			return JsonResponse(serializer.data, safe=False)

	@auth_required
	def post(self, request):
		msg = request.POST['msg']
		if msg != '':
			msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + str(datetime.now().strftime("%d %b %Y"))[:11]
			author = get_object_or_404(UserProfile, id=request.user.id)
			friend = get_object_or_404(UserProfile, id=request.POST['friend_id'])
			author_f_name_l_name = author.first_name[0] + author.last_name[0]
			try:
				chat_room = ChatRoom.objects.get(author__id=author.id, friend__id=friend.id)
			except ChatRoom.DoesNotExist:
				room_data = {
					'author': author,
					'friend': friend,
					'author_id': author.id,
					'friend_id': friend.id,
					'logo': friend.user_logo
				}
				chat_room = functions.create_chat_room(room_data)
			message_data = {
				'chat_room': chat_room,
				'message': msg,
				'message_time': msg_time,
				'author_username': author.username,
				'author_initials': author_f_name_l_name,
				'author_logo': author.user_logo,
				'author_id': author.id
			}
			functions.create_message(message_data)
			if author.id != friend.id:
				try:
					chat_room = ChatRoom.objects.get(author__id=friend.id, friend__id=author.id)
				except ChatRoom.DoesNotExist:
					room_data = {
						'author': friend,
						'friend': author,
						'author_id': friend.id,
						'friend_id': author.id,
						'logo': author.user_logo
					}
					chat_room = functions.create_chat_room(room_data)
				message_data = {
					'chat_room': chat_room,
					'message': msg,
					'message_time': msg_time,
					'author_username': author.username,
					'author_initials': author_f_name_l_name,
					'author_logo': author.user_logo,
					'author_id': author.id
				}
				functions.create_message(message_data)
			return JsonResponse({'status_message': 'Message has been sent!'})
		return JsonResponse({'status_message': 'Message is empty!'})


def send_email(request):
	if request.user.is_authenticated:
		return redirect('index')
	if 'generated_code' in request.GET and 'user_email' in request.GET:
		usr_email = request.GET['user_email']
		if not functions.check_email(usr_email, UserProfile.objects.all()):
			return JsonResponse({
				'error_code': "222",
				'name': "User with this email address already exists!"
			})
		g_c = request.GET['generated_code']
		request.session['gen_code'] = g_c
		message_content = """This is data for signing in Your account:\n\n Login:           {}\n Password:    {}\n\n
Do not show this message to anyone to prevent stealing your account!\n\n\n
The last step you should perform is to enter this code: "{}".\n\n\n
Thank You for registering on our website.\n
Best regards, messenger support.""".format(
			request.GET['username'],
			request.GET['password'],
			g_c
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
