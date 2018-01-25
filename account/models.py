from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import date
from django.core.exceptions import ObjectDoesNotExist


class UserProfile(User):
	user = models.OneToOneField(User)
	logo = models.ImageField(default='logo_none.jpg')
	gender = models.CharField(max_length=6, blank=True)
	birthday = models.DateField(default=date.today)
	country = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=50, blank=True)
	mobile_number = models.CharField(max_length=10, blank=True)
	about = models.CharField(max_length=999999, blank=True)
	education = models.CharField(max_length=100, blank=True)

	@staticmethod
	def get_by_id(user_id):
		try:
			user_profile = UserProfile.objects.get(id=user_id)
			return user_profile
		except ObjectDoesNotExist:
			return None
	
	@staticmethod
	def filter_by(user=None, gender=None, birthday=None, country=None, city=None, education=None, **kwargs):
		query = {}
		if user:
			query['user'] = user
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
		try:
			profiles = UserProfile.objects.filter(**query)
			return profiles
		except ObjectDoesNotExist:
			return None
	
	@staticmethod
	def add(first_name, last_name, username, password, email, city=None, country=None, birthday=None, gender=None,
			education=None,	mobile=None, about=None, **kwargs):
		user_profile = UserProfile()
		user_profile.user = User.objects.create_user(username=username, email=email, password=password)
		user_profile.first_name = first_name
		user_profile.last_name = last_name
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
		user_profile.user.save()
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
		except ObjectDoesNotExist:
			return None
