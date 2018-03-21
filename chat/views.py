from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from account.models import UserProfile
from chat.models import Message, ChatRoom
from utils.view_modifiers import auth_required
from utils.responses import NOT_FOUND, BAD_REQUEST, OK


class IndexView(View):

	template_name = 'home.html'
	
	def get(self, request):
		return render(request, self.template_name)


class ChatListView(View):
	
#	@auth_required
	def get(self, request):
		if 'author_id' in request.GET:
			user_id = request.GET.get('author_id')
		else:
			return BAD_REQUEST
		author = UserProfile.get_by_id(user_id)
		response = {
			'data': {
				'chats': [x.to_dict() for x in ChatRoom.filter_by(author=author)]
			},
			'status': "OK"
		}
		return JsonResponse(response, status=200, safe=False)

#	@auth_required
	def post(self, request):
		if 'id' in request.POST:
			data = {
				'author': UserProfile.get_by_id(request.user.id),
				'friend': UserProfile.get_by_id(request.POST.get('id'))
			}
			chat_room = ChatRoom.filter_by(**data)
		else:
			data = {
				# TODO: get storage
			}
			chat_room = None
		if chat_room:
			chat_room.first().delete()
			response = {
				'success': 'Chat room has been deleted.'
			}
			return JsonResponse(response, status=201, safe=False)
		else:
			return NOT_FOUND


class ChatRoomView(View):
	
#	@auth_required
	def get(self, request):
		if 'friend_id' not in request.GET:
			data = {
				'author': UserProfile.get_by_id(request.user.id),
				'friend': UserProfile.get_by_id(request.GET.get('friend_id'))
			}
			chat_room = ChatRoom.filter_by(**data)
		else:
			data = {
				# TODO: get storage
			}
			chat_room = None
		if chat_room:
			filter_data = {
				'chat_room': chat_room.first()
			}
			messages = Message.filter_by(**filter_data)
			offset = len(messages)
			if 'offset' in request.GET:
				offset = int(request.GET.get('offset'))
			if offset <= len(messages):
				messages = messages[len(messages) - offset:]
			else:
				return BAD_REQUEST
			response = {
				'data': {
					'messages': [message.to_dict() for message in messages]
				},
				'status': 'OK'
			}
			return JsonResponse(response, status=200, safe=False)
		else:
			return NOT_FOUND
	
#	@auth_required
	def post(self, request):
		msg = request.POST.get('msg')
		if msg != '':
			msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + str(
				datetime.now().strftime("%d %b %Y"))[:11]
			author = UserProfile.get_by_id(request.user.id)
			friend = UserProfile.get_by_id(request.POST.get('friend_id'))
			if not author and not friend:
				return NOT_FOUND
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
			return OK
		return BAD_REQUEST
