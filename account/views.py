from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

from utils import header
from chat.models import ChatRoom, Message
from .models import UserProfile, Photo
from utils.view_modifiers import auth_required
from utils.helpers import email_does_not_exist
from utils.responses import NOT_FOUND, BAD_REQUEST, CREATED, OK


class Profile(View):
	
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

#	@auth_required
	def post(self, request):
		if 'avatar' in request.FILES:
			user_profile = UserProfile.filter_by(pk=request.user.id)
			if not user_profile:
				return NOT_FOUND
			user_profile = user_profile.first()
			request_logo = request.FILES['avatar']
			user_profile.avatar = request_logo
			user_profile.save()
			chat_rooms = ChatRoom.filter_by(friend=user_profile)
			if chat_rooms:
				for room in chat_rooms:
					room.logo = request_logo
					room.save()
			messages = Message.filter_by(author=user_profile)
			if messages:
				for message in messages:
					message.author_logo = request_logo
					message.save()
			data = {
				'author': user_profile,
				'photo': request_logo
			}
			photo = Photo.add(**data)
			response = {
				'data': {
					'avatar': photo.to_dict()
				},
				'status': 'CREATED'
			}
			return JsonResponse(response, status=201, safe=False)
		else:
			return BAD_REQUEST


class EditUserProfile(View):

	def get(self, request):
		return BAD_REQUEST
	
#	@auth_required
	def post(self, request, profile_id):
		data = {
			'first_name': request.POST.get('first_name'),
			'last_name': request.POST.get('last_name'),
			'mobile': request.POST.get('mobile_number'),
			'bio': request.POST.get('about_me'),
			'username': request.POST.get('username'),
			'avatar': request.POST.get('avatar')
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
		
		
class RegistrationView(View):
	
	def get(self, request):
		return BAD_REQUEST
	
	def post(self, request):
		form = request.POST
		for key in ['first_name', 'last_name', 'email', 'username', 'password', 'code']:
			if key not in form.keys():
				break
		else:
			first_name = form.get('first_name')
			last_name = form.get('last_name')
			username = form.get('username')
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
					'username': username,
					'email': email,
					'password': password
				}
				UserProfile.add(**data)
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						return CREATED
		return BAD_REQUEST


class LoginView(View):

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


def logout_user(request):
	logout(request)
	return OK
