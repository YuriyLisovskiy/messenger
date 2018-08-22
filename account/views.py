from django.http import JsonResponse
from django.views.generic import View

from .models import UserProfile, Photo
from chat.models import Dialog, Message
from utils.responses import NOT_FOUND, BAD_REQUEST


class GetProfile(View):
	
#	@auth_required
	def get(self, request):
		if 'id' in request.GET:
			user_id = request.GET.get('id')
		else:
			user_id = request.user.id
		user_profile = UserProfile.get_by_id(user_id)
		if user_profile:
			user_logos = Photo.filter_by(author=user_profile)
			response = {
				'data': {
					'profile': user_profile.to_dict(),
					'avatars': [x.to_dict() for x in user_logos]
				},
				'status': 'OK'
			}
			return JsonResponse(response, status=200, safe=False)
		return NOT_FOUND

	def post(self, request):
		return BAD_REQUEST


class UpdateProfile(View):

	def get(self, request):
		return BAD_REQUEST
	
#	@auth_required
	def post(self, request):
		profile_id = request.POST.get('id')
		if not profile_id:
			return BAD_REQUEST
		user_profile = UserProfile.filter_by(pk=profile_id).first()
		if not user_profile:
			return BAD_REQUEST
		avatar = None
		if 'avatar' in request.FILES:
			avatar = request.FILES['avatar']
			chat_rooms = Dialog.filter_by(friend=user_profile)
			if chat_rooms:
				for room in chat_rooms:
					room.logo = avatar
					room.save()
			messages = Message.filter_by(author_id=user_profile.id)
			if messages:
				for message in messages:
					message.author_logo = avatar
					message.save()
		data = {
			'first_name': request.POST.get('first_name'),
			'last_name': request.POST.get('last_name'),
			'mobile': request.POST.get('mobile_number'),
			'bio': request.POST.get('about_me'),
			'username': request.POST.get('username'),
			'avatar': avatar
		}
		profile = UserProfile.edit(profile_id, **data)
		if profile:
			response = {
				'data': {
					'profile': profile.to_dict()
				},
				'status': 'CREATED'
			}
			return JsonResponse(response, status=201, safe=False)
		return NOT_FOUND
