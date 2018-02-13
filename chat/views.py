from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from account.models import UserProfile
from chat.models import Message, ChatRoom
from utils.view_modifiers import auth_required
from utils.responses import NOT_FOUND, BAD_REQUEST


class IndexView(View):

	template_name = 'home.html'
	
	def get(self, request):
		return render(request, self.template_name)


class ChatListView(View):
	
#	@auth_required
	def get(self, request):
		response = {
			'data': {
				'user_id': request.user.id,
				'user_list': [x.to_dict for x in UserProfile.get_all()],
				'chat_room_list': [x.to_dict for x in ChatRoom.get_all()]
			}
		}
		return JsonResponse(response, status=200, safe=False)

#	@auth_required
	def post(self, request):
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
			return JsonResponse(response, status=201, safe=False)
		else:
			return NOT_FOUND()


class ChatRoomView(View):
	
#	@auth_required
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
	
#	@auth_required
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
