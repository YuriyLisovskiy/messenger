from django.http import JsonResponse
from django.views.generic import View

from .models import UserProfile, Photo
from chat.models import Dialog, Message
from utils.view_modifiers import auth_required
from utils.responses import NOT_FOUND, BAD_REQUEST


# Returns user profile.
#
# Method: GET
# API url: /api/v1/account/getProfile
# Required params:
#   - 'id': int (required)
class GetProfile(View):
	
	@auth_required
	def get(self, request):
		if 'id' in request.GET:
			user_id = request.GET.get('id')
			user_profile = UserProfile.get_by_id(user_id)
			if user_profile:
				user_logos = Photo.filter_by(author=user_profile)
				response = {
					'data': {
						'profile': user_profile.to_dict(),
						'images': [x.to_dict() for x in user_logos]
					},
					'status': 'OK'
				}
				return JsonResponse(response, status=200, safe=False)
			return NOT_FOUND
		return BAD_REQUEST

	@staticmethod
	def post():
		return BAD_REQUEST


# Updates user profile.
#
# Method: POST
# API url: /api/v1/account/updateProfile
# Required params:
#   - 'id': int (required)
#   - 'avatar': file (optional)
#   - 'first_name': str (optional)
#   - 'last_name': str (optional)
#   - 'mobile': str (optional)
#   - 'bio': str (optional)
#   - 'username': str (optional)
class UpdateProfile(View):
	
	@staticmethod
	def get():
		return BAD_REQUEST
	
	@auth_required
	def post(self, request):
		if 'id' in request.POST:
			profile_id = request.POST.get('id')
			user_profile = UserProfile.filter_by(pk=profile_id).first()
			if not user_profile:
				return BAD_REQUEST
			avatar = None
			if 'avatar' in request.FILES:
				avatar = request.FILES['avatar']
				dialogs = Dialog.filter_by(friend=user_profile)
				if dialogs:
					for dialog in dialogs:
						dialog.logo = avatar
						dialog.save()
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
		return BAD_REQUEST
