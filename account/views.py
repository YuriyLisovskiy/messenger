from datetime import datetime
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from .models import UserProfile, PhotoLogo
from chat.models import ChatRoom, Message
from utils import header
from utils.helpers import password_is_valid, username_is_valid, email_does_not_exist
from utils.responses import NOT_FOUND, BAD_REQUEST
from utils.view_modifiers import auth_required


class Profile(View):
	
	template_name = 'account/user_profile.html'
	
	@auth_required
	def get(self, request, profile_id):
		user_profile = UserProfile.get_by_id(profile_id)
		if user_profile:
			if user_profile.country != '':
				user_profile.country = header.CountryList().get_county(user_profile.country)
			user_logos = PhotoLogo.filter_by(owner=user_profile)
			return render(request, self.template_name, {
				'user_profile': user_profile,
				'user_logos': user_logos,
			})
		return NOT_FOUND()

	@auth_required
	def post(self, request, profile_id):
		if 'message' in request.POST:
			author_id, friend_id = request.POST['data'].split()
			msg = request.POST['message']
			author = UserProfile.filter_by(pk=author_id)
			friend = UserProfile.filter_by(id=friend_id)
			if not author or not friend:
				return BAD_REQUEST()
			author = author.first()
			friend = friend.first()
			msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + datetime.now().strftime("%d %b %Y")[:11]
			filter_data = {
				'author': author,
				'friend': friend
			}
			author_chat_room = ChatRoom.filter_by(**filter_data)
			filter_data = {
				'author': friend,
				'friend': author
			}
			friend_chat_room = ChatRoom.filter_by(**filter_data)
			if not author_chat_room and not friend_chat_room:
				if author == friend:
					room_data = {
						'author': author,
						'friend': author,
						'logo': author.user_logo
					}
					chat_room = ChatRoom.add(**room_data)
					if msg != "":
						message_data = {
							'chat_room': chat_room,
							'author': author,
							'msg': msg,
							'time': msg_time,
						}
						Message.add(**message_data)
					return redirect('/account/user/id=' + str(request.user.id))
				room_data = {
					'author': author,
					'friend': friend,
					'logo': friend.user_logo
				}
				chat_room = ChatRoom.add(**room_data)
				if msg != "":
					message_data = {
						'chat_room': chat_room,
						'author': author,
						'mag': msg,
						'time': msg_time,
					}
					Message.add(**message_data)
				room_data = {
					'author': friend,
					'friend': author,
					'logo': author.user_logo
				}
				ChatRoom.add(**room_data)
				if msg != "":
					message_data = {
						'chat_room': chat_room,
						'author': author,
						'msg': msg,
						'time': msg_time,
					}
					Message.add(**message_data)
					return redirect('/account/user/id=' + str(request.user.id))
			if msg != "":
				if author_chat_room:
					message_data = {
						'chat_room': author_chat_room,
						'author': author,
						'msg': msg,
						'time': msg_time,
					}
					Message.add(**message_data)
					if not friend_chat_room:
						room_data = {
							'author': friend,
							'friend': author,
							'logo': author.user_logo
						}
						chat_room = ChatRoom.add(**room_data)
						message_data = {
							'chat_room': chat_room,
							'author': author,
							'msg': msg,
							'time': msg_time,
						}
						Message.add(**message_data)
				if friend_chat_room:
					if author_chat_room != friend_chat_room:
						message_data = {
							'chat_room': friend_chat_room,
							'author': author,
							'msg': msg,
							'time': msg_time,
						}
						Message.add(**message_data)
						if not author_chat_room:
							room_data = {
								'author': author,
								'friend': friend,
								'logo': friend.user_logo
							}
							chat_room = ChatRoom.add(**room_data)
							message_data = {
								'chat_room': chat_room,
								'author': author,
								'msg': msg,
								'time': msg_time,
							}
							Message.add(**message_data)
					return redirect('/account/user/id=' + str(request.user.id))
				return redirect('/account/user/id=' + str(request.user.id))
			return redirect('/account/user/id=' + str(request.user.id))
		elif 'logo' in request.FILES:
			user_profile = UserProfile.filter_by(pk=request.user.id)
			if not user_profile:
				return NOT_FOUND()
			user_profile = user_profile.first()
			upload_time = str(datetime.now())[11:16] + "  |  " + str(datetime.now().strftime("%d %b %Y"))[:11]
			request_logo = request.FILES['logo']
			user_profile.logo = request_logo
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
				'owner': user_profile,
				'photo': request_logo,
				'upload_time': upload_time
			}
			PhotoLogo.add(**data)
			return redirect('/account/user/id=' + str(request.user.id))
		else:
			return BAD_REQUEST()


class EditUserProfile(View):

	template_name = 'account/edit_profile.html'
	
	@auth_required
	def get(self, request, profile_id):
		user = UserProfile.get_by_id(profile_id)
		if user:
			if user.country:
				user.country = header.COUNTRY_LIST.get_county(user.country)
			context = {
				'user_data': user,
				'country_list': header.COUNTRY_LIST.country_list()
			}
			return render(request, self.template_name, context)
		return NOT_FOUND()

	@auth_required
	def post(self, request, profile_id):
		country = request.POST.get('country')
		if country:
			if country != '':
				country = header.COUNTRY_LIST.get_iso_code(country)
		data = {
			'first_name': request.POST.get('first_name'),
			'last_name': request.POST.get('last_name'),
			'city': request.POST.get('city'),
			'country': country,
			'birthday': request.POST.get('birthday'),
			'gender': request.POST.get('gender'),
			'education': request.POST.get('education'),
			'mobile': request.POST.get('mobile_number'),
			'about': request.POST.get('about_me'),
		}
		user = UserProfile.edit(profile_id, **data)
		if user:
			if user.country or user.country != '':
				user.country = header.COUNTRY_LIST.get_county(user.country)
			return render(request, self.template_name, {
				'user_data': user,
				'country_list': header.COUNTRY_LIST.country_list(),
				'response_msg': 'Profile changes has been saved.'
			})
		return NOT_FOUND()
		
		
class RegistrationView(View):
	
	template_name = 'account/register.html'

	def get(self, request):
		if request.user.is_authenticated:
			return redirect('index')
		return render(request, self.template_name)

	def post(self, request):
		if request.user.is_authenticated:
			return redirect('/account/user/id=' + str(UserProfile.filter_by(pk=request.user.id).first().id))
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
			if not username_is_valid(username):
				errors['username'] = 'username must be 3 characters or more'
			if not email_does_not_exist(email, UserProfile.objects.all()):
				errors['email'] = 'account with this email address already exists'
			if not password_is_valid(password):
				errors['password'] = 'password must be 8 characters or more'
			if generated_code != request.session['gen_code']:
				errors['code'] = 'incorrect received code'
			if len(errors) > 0:
				return render(request, self.template_name, errors)
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
						return render(request, "chat/index.html", {'response_msg': 'Thank you for joining us :)'})
			return render(request, self.template_name)
		return BAD_REQUEST()


def logout_user(request):
	logout(request)
	return redirect('login')


def login_user(request):
	login_form = 'account/login_form.html'
	if request.method == 'GET':
		if request.user.is_authenticated:
			return redirect('/account/user/id=' + str(request.user.id))
		return render(request, login_form)
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username and password:
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/account/user/id=' + str(request.user.id))
				else:
					context = {
						'error_message': 'Your account has been disabled'
					}
			else:
				context = {
					'error_message': 'Invalid login or password'
				}
			return render(request, login_form, context)
	return BAD_REQUEST()
