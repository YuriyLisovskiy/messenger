from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class UserProfile(User):
	avatar = models.ImageField(blank=True)
	mobile_number = models.CharField(max_length=10, blank=True)
	bio = models.CharField(max_length=256, blank=True)

	def to_dict(self):
		context = {
			'id': self.id,
			'superuser': self.is_superuser,
			'username': self.username,
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'mobile_number': self.mobile_number,
			'bio': self.bio,
		}
		if self.avatar:
			context['avatar'] = self.avatar.url
		return context

	@staticmethod
	def get_by_id(user_id):
		try:
			user_profile = UserProfile.objects.get(id=user_id)
			return user_profile
		except ObjectDoesNotExist:
			return None
	
	@staticmethod
	def filter_by(first_name=None, last_name=None, username=None, email=None, mobile_number=None, **kwargs):
		query = {}
		if first_name:
			query['first_name'] = first_name
		if last_name:
			query['last_name'] = last_name
		if username:
			query['username'] = username
		if email:
			query['email'] = email
		if mobile_number:
			query['mobile_number'] = mobile_number
		query.update(**kwargs)
		return UserProfile.objects.filter(**query)
		
	@staticmethod
	def get_all():
		return UserProfile.objects.all()
	
	@staticmethod
	def add(first_name, last_name, username, password, email, mobile=None, bio=None, avatar=None):
		user_profile = UserProfile()
		user_profile.first_name = first_name
		user_profile.last_name = last_name
		user_profile.email = email
		user_profile.username = username
		user_profile.set_password(password)
		if mobile:
			user_profile.mobile_number = mobile
		if bio:
			user_profile.bio = bio
		if avatar:
			user_profile.avatar = avatar
		user_profile.save()
		return user_profile

	@staticmethod
	def edit(pk, first_name=None, last_name=None, mobile=None, bio=None, username=None, avatar=None):
		user = UserProfile.get_by_id(pk)
		if not user:
			return None
		if first_name:
			user.first_name = first_name
		if last_name:
			user.last_name = last_name
		if username:
			user.username = username
		if mobile:
			user.mobile_number = mobile
		if bio:
			user.bio = bio
		if avatar:
			user.avatar = avatar
		user.save()
		return user
		

class Photo(models.Model):
	author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
	photo = models.ImageField()
	
	def to_dict(self):
		return {
			'author_id': self.author.id,
			'photo': self.photo.url
		}
	
	@staticmethod
	def get_by_id(pk):
		try:
			photo = Photo.objects.get(pk=pk)
			return photo
		except ObjectDoesNotExist:
			return None
		
	@staticmethod
	def get_all():
		return Photo.objects.all()
		
	@staticmethod
	def filter_by(author=None, photo=None, **kwargs):
		query = {}
		if author:
			query['author'] = author
		if photo:
			query['photo'] = photo
		query.update(**kwargs)
		return Photo.objects.filter(**query)
	
	@staticmethod
	def add(author, photo):
		new_photo = Photo()
		new_photo.author = author
		new_photo.photo = photo
		new_photo.save()
		return new_photo
	
	@staticmethod
	def edit(pk, author=None, photo=None):
		photo_to_edit = Photo.get_by_id(pk)
		if not photo_to_edit:
			return None
		if author:
			photo_to_edit.author = author
		if photo:
			photo_to_edit.photo = photo
		photo_to_edit.save()
		return photo_to_edit
