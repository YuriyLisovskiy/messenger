from django.shortcuts import render

from .models import ChatRoom
from account.models import UserProfile
from utils.view_modifiers import auth_required


def index(request):
	return render(request, 'index.html')


@auth_required
def chat(request):
	user = request.user
	all_users = UserProfile.get_all()
	all_chat_rooms = ChatRoom.get_all()
	return render(request, 'chat/chat.html', {
		'user': user,
		'all_users': all_users,
		'all_chat_rooms': all_chat_rooms
	})
