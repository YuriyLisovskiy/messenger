from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet


class UserProfile(User):
	logo = models.ImageField(blank=True)
	gender = models.CharField(max_length=6, blank=True)
	birthday = models.DateField(blank=True, null=True)
	country = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=50, blank=True)
	mobile_number = models.CharField(max_length=10, blank=True)
	about = models.CharField(max_length=999999, blank=True)
	education = models.CharField(max_length=100, blank=True)

	def to_dict(self):
		context = {
			'id': self.id,
			'username': self.username,
			'email': self.email,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'gender': self.gender,
			'birthday': self.birthday,
			'country': self.country,
			'city': self.city,
			'mobile_number': self.mobile_number,
			'about': self.about,
			'education': self.education
		}
		if self.logo:
			context['logo'] = self.logo.url
		return context

	@staticmethod
	def get_by_id(user_id):
		try:
			user_profile = UserProfile.objects.get(id=user_id)
			return user_profile
		except ObjectDoesNotExist:
			return None
	
	@staticmethod
	def filter_by(first_name=None, last_name=None, gender=None, birthday=None, country=None, city=None,
				education=None, **kwargs):
		query = {}
		if first_name:
			query['first_name'] = first_name
		if last_name:
			query['last_name'] = last_name
		if gender:
			query['gender'] = gender
		if birthday:
			query['birthday'] = birthday
		if country:
			query['country'] = country
		if city:
			query['city'] = city
		if education:
			query['education'] = education
		query.update(**kwargs)
		return UserProfile.objects.filter(**query)
		
	@staticmethod
	def get_all():
		return UserProfile.objects.all()
	
	@staticmethod
	def add(first_name, last_name, username, password, email, city=None, country=None, birthday=None, gender=None,
			education=None,	mobile=None, about=None, **kwargs):
		user_profile = UserProfile()
		user_profile.first_name = first_name
		user_profile.last_name = last_name
		user_profile.email = email
		user_profile.username = username
		user_profile.set_password(password)
		if city:
			user_profile.city = city
		if country:
			user_profile.country = country
		if gender:
			user_profile.gender = gender
		if education:
			user_profile.education = education
		if mobile:
			user_profile.mobile_number = mobile
		if about:
			user_profile.about = about
		if birthday:
			user_profile.birthday = birthday
		user_profile.save()
		return user_profile

	@staticmethod
	def edit(pk, first_name=None, last_name=None, city=None, country=None, birthday=None, gender=None, education=None,
			mobile=None, about=None):
		user = UserProfile.get_by_id(pk)
		if not user:
			return None
		if first_name:
			user.first_name = first_name
		if last_name:
			user.last_name = last_name
		if city:
			user.city = city
		if country:
			user.country = country
		if gender:
			user.gender = gender
		if education:
			user.education = education
		if mobile:
			user.mobile_number = mobile
		if about:
			user.about = about
		if birthday:
			user.birthday = birthday
		user.save()
		return user
		

class PhotoLogo(models.Model):
	owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
	photo = models.ImageField()
	upload_time = models.CharField(default="", max_length=100)
	
	@staticmethod
	def get_by_id(pk):
		try:
			photo = PhotoLogo.objects.get(pk=pk)
			return photo
		except ObjectDoesNotExist:
			return None
		
	@staticmethod
	def get_all():
		try:
			photo = PhotoLogo.objects.all()
			return photo
		except EmptyResultSet:
			return None
		
	@staticmethod
	def filter_by(owner=None, img=None, upload_time=None, **kwargs):
		query = {}
		if owner:
			query['owner'] = owner
		if img:
			query['photo'] = img
		if upload_time:
			query['upload_time'] = upload_time
		query.update(**kwargs)
		try:
			photos = PhotoLogo.objects.filter(**query)
			return photos
		except EmptyResultSet:
			return None
	
	@staticmethod
	def add(owner, photo, upload_time, **kwargs):
		new_photo = PhotoLogo()
		new_photo.owner = owner
		new_photo.photo = photo
		new_photo.upload_time = upload_time
		new_photo.save()
		return new_photo
	
	@staticmethod
	def edit(pk, owner=None, photo=None, upload_time=None, **kwargs):
		photo_to_edit = PhotoLogo.get_by_id(pk)
		if not photo_to_edit:
			return None
		if owner:
			photo_to_edit.owner = owner
		if photo:
			photo_to_edit.photo = photo
		if upload_time:
			photo_to_edit.upload_time = upload_time
		photo_to_edit.save()
		return photo_to_edit
