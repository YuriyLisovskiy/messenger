from django.shortcuts import render
from django.views.generic import View

from .models import ChatRoom
from account.models import UserProfile
from utils.view_modifiers import auth_required


class IndexView(View):

	template_name = 'index.html'
	
	def get(self, request):
		return render(request, self.template_name)


class ChatView(View):
	
	template_name = 'chat/chat.html'
	
	@auth_required
	def get(self, request):
		context = {
			'user': request.user,
			'all_users': UserProfile.get_all(),
			'all_chat_rooms': ChatRoom.get_all()
		}
		return render(request, template_name=self.template_name, context=context)
