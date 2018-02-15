import os
import glob

from unittest import skip
from django.test import TestCase
from django.core.files.images import ImageFile
from django.utils.datetime_safe import datetime

from account.models import UserProfile, Photo


@skip
class TestUserProfile(TestCase):
	
	def setUp(self):
		self.birthday = datetime.strptime('2014-12-04', '%Y-%m-%d').date()
		data = {
			'first_name': 'some_first_name',
			'last_name': 'some_last_name',
			'username': 'some_username',
			'email': 'some.email@gmail.com',
			'password': 'super_safe_password',
			'city': 'some_city',
			'country': 'some_country',
			'birthday': self.birthday,
			'gender': 'Male',
			'education': 'some_education',
			'mobile': '1234567890',
			'about': 'some interesting data'
		}
		user = UserProfile.add(**data)
		self.id = user.id
	
	def test_add(self):
		birthday = datetime.strptime('2017-12-04', '%Y-%m-%d').date()
		data = {
			'first_name': 'another_first_name',
			'last_name': 'another_last_name',
			'username': 'another_username',
			'email': 'another.email@gmail.com',
			'password': 'super_safe_password',
			'city': 'another_city',
			'country': 'another_country',
			'birthday': birthday,
			'gender': 'Female',
			'education': 'another_education',
			'mobile': '0987654321',
			'about': 'another interesting data'
		}
		user_id = UserProfile.add(**data).id
		user = UserProfile.get_by_id(user_id)
		self.assertEqual(user.id, user_id)
		self.assertEqual(user.first_name, 'another_first_name')
		self.assertEqual(user.last_name, 'another_last_name')
		self.assertEqual(user.username, 'another_username')
		self.assertEqual(user.email, 'another.email@gmail.com')
		self.assertEqual(user.city, 'another_city')
		self.assertEqual(user.country, 'another_country')
		self.assertEqual(user.birthday, birthday)
		self.assertEqual(user.gender, 'Female')
		self.assertEqual(user.education, 'another_education')
		self.assertEqual(user.mobile_number, '0987654321')
		self.assertEqual(user.about, 'another interesting data')
		self.assertEqual(user.logo.name, '')
	
	def test_edit(self):
		user_id = UserProfile.get_by_id(self.id).id
		user = UserProfile.get_by_id(user_id)
		self.assertEqual(user.first_name, 'some_first_name')
		self.assertEqual(user.last_name, 'some_last_name')
		self.assertEqual(user.username, 'some_username')
		self.assertEqual(user.email, 'some.email@gmail.com')
		self.assertEqual(user.city, 'some_city')
		self.assertEqual(user.country, 'some_country')
		self.assertEqual(user.birthday, self.birthday)
		self.assertEqual(user.gender, 'Male')
		self.assertEqual(user.education, 'some_education')
		self.assertEqual(user.mobile_number, '1234567890')
		self.assertEqual(user.about, 'some interesting data')
		self.assertEqual(user.logo.name, '')
		birthday = datetime.strptime('2000-12-04', '%Y-%m-%d').date()
		data = {
			'first_name': 'first_name',
			'last_name': 'last_name',
			'city': 'city',
			'country': 'country',
			'birthday': birthday,
			'gender': 'Female',
			'education': 'education',
			'mobile': '0000000000',
			'about': 'interesting data'
		}
		user = UserProfile.edit(pk=100500, **data)
		self.assertEqual(user, None)
		UserProfile.edit(pk=user_id, **data)
		user = UserProfile.get_by_id(user_id)
		self.assertEqual(user.id, user_id)
		self.assertEqual(user.first_name, 'first_name')
		self.assertEqual(user.last_name, 'last_name')
		self.assertEqual(user.username, 'some_username')
		self.assertEqual(user.email, 'some.email@gmail.com')
		self.assertEqual(user.city, 'city')
		self.assertEqual(user.country, 'country')
		self.assertEqual(user.birthday, birthday)
		self.assertEqual(user.gender, 'Female')
		self.assertEqual(user.education, 'education')
		self.assertEqual(user.mobile_number, '0000000000')
		self.assertEqual(user.about, 'interesting data')
		self.assertEqual(user.logo.name, '')
	
	def test_filter_by(self):
		birthday = datetime.strptime('2014-12-04', '%Y-%m-%d').date()
		data = {
			'first_name': 'some_first_name',
			'last_name': 'another_last_name',
			'username': 'another_username',
			'email': 'another.email@gmail.com',
			'password': 'super_safe_password',
			'city': 'some_city',
			'country': 'another_country',
			'birthday': birthday,
			'gender': 'Female',
			'education': 'some_education',
			'mobile': '0987654321',
			'about': 'another interesting data'
		}
		UserProfile.add(**data)
		filter_data = {
			'first_name': 'first_name'
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 0)
		filter_data = {
			'first_name': 'some_first_name'
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 2)
		filter_data = {
			'last_name': 'some_last_name'
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 1)
		filter_data = {
			'city': 'some_city'
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 2)
		filter_data = {
			'country': 'some_country'
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 1)
		filter_data = {
			'birthday': birthday
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 2)
		
		filter_data = {
			'gender': 'Male'
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 1)
		filter_data = {
			'education': 'some_education'
		}
		users = UserProfile.filter_by(**filter_data)
		self.assertEqual(len(users), 2)
		
	def test_get_by_id(self):
		self.assertEqual(UserProfile.get_by_id(100), None)
		user = UserProfile.get_by_id(self.id)
		self.assertEqual(user.id, self.id)
		self.assertEqual(user.first_name, 'some_first_name')
		self.assertEqual(user.last_name, 'some_last_name')
		self.assertEqual(user.username, 'some_username')
		self.assertEqual(user.email, 'some.email@gmail.com')
		self.assertEqual(user.city, 'some_city')
		self.assertEqual(user.country, 'some_country')
		self.assertEqual(user.birthday, self.birthday)
		self.assertEqual(user.gender, 'Male')
		self.assertEqual(user.education, 'some_education')
		self.assertEqual(user.mobile_number, '1234567890')
		self.assertEqual(user.about, 'some interesting data')
		self.assertEqual(user.logo.name, '')
	
	def test_to_dict(self):
		user = UserProfile.get_by_id(self.id)
		user.logo = self.IMAGE_FILE()
		user_dict = user.to_dict()
		self.assertEqual(user_dict['id'], self.id)
		self.assertEqual(user_dict['first_name'], 'some_first_name')
		self.assertEqual(user_dict['last_name'], 'some_last_name')
		self.assertEqual(user_dict['username'], 'some_username')
		self.assertEqual(user_dict['email'], 'some.email@gmail.com')
		self.assertEqual(user_dict['city'], 'some_city')
		self.assertEqual(user_dict['country'], 'some_country')
		self.assertEqual(user_dict['birthday'], self.birthday)
		self.assertEqual(user_dict['gender'], 'Male')
		self.assertEqual(user_dict['education'], 'some_education')
		self.assertEqual(user_dict['mobile_number'], '1234567890')
		self.assertEqual(user_dict['about'], 'some interesting data')
		self.assertEqual(user_dict['logo'], user.logo.url)
	
	def test_get_all(self):
		users = UserProfile.get_all()
		self.assertEqual(len(users), 1)
		data = {
			'first_name': 'another_first_name',
			'last_name': 'another_last_name',
			'username': 'another_username',
			'email': 'another.email@gmail.com',
			'password': 'super_safe_password',
		}
		user_id = UserProfile.add(**data).id
		users = UserProfile.get_all()
		self.assertEqual(len(users), 2)
		UserProfile.get_by_id(self.id).delete()
		UserProfile.get_by_id(user_id).delete()
		users = UserProfile.get_all()
		self.assertEqual(len(users), 0)
		
	def tearDown(self):
		try:
			os.remove('media/test.png')
		except OSError:
			pass
		try:
			os.remove('media/temp.png')
		except OSError:
			pass
		for file in glob.glob('media/test_*.png'):
			os.remove(file)
		for file in glob.glob('media/temp_*.png'):
			os.remove(file)
	
	@staticmethod
	def IMAGE_FILE(name='test.png'):
		img = ImageFile(open(name, 'w+'), name)
		os.remove(name)
		return img


@skip
class TestPhotoLogo(TestCase):
	
	def setUp(self):
		data = {
			'first_name': 'another_first_name',
			'last_name': 'another_last_name',
			'username': 'another_username',
			'email': 'another.email@gmail.com',
			'password': 'super_safe_password',
		}
		self.user = UserProfile.add(**data)
		data = {
			'owner': self.user,
			'photo': self.IMAGE_FILE('temp.png'),
			'upload_time': 'time'
		}
		self.id = Photo.add(**data).id
	
	def test_add(self):
		data = {
			'owner': self.user,
			'photo': self.IMAGE_FILE(),
			'upload_time': 'another_time'
		}
		photo_id = Photo.add(**data).id
		photo = Photo.get_by_id(photo_id)
		self.assertEqual(photo.owner, self.user)
		self.assertEqual(photo.photo, self.IMAGE_FILE())
		self.assertEqual(photo.upload_time, 'another_time')
	
	def test_edit(self):
		photo = Photo.get_by_id(100500)
		self.assertEqual(photo, None)
		photo = Photo.get_by_id(self.id)
		self.assertEqual(photo.owner, self.user)
		self.assertEqual(photo.photo, self.IMAGE_FILE('temp.png'))
		self.assertEqual(photo.upload_time, 'time')
		data = {
			'first_name': 'some_first_name',
			'last_name': 'some_last_name',
			'username': 'some_username',
			'email': 'some.email@gmail.com',
			'password': 'super_safe_password',
		}
		user = UserProfile.add(**data)
		data = {
			'owner': user,
			'photo': self.IMAGE_FILE(),
			'upload_time': 'some_time'
		}
		photo = Photo.edit(pk=100500, **data)
		self.assertEqual(photo, None)
		Photo.edit(pk=self.id, **data)
		photo = Photo.get_by_id(self.id)
		self.assertEqual(photo.owner, user)
		self.assertEqual(photo.photo, self.IMAGE_FILE())
		self.assertEqual(photo.upload_time, 'some_time')
	
	def test_filter_by(self):
		data = {
			'owner': self.user,
			'photo': self.IMAGE_FILE(),
			'upload_time': 'time_1'
		}
		Photo.add(**data)
		filter_data = {
			'owner': self.user
		}
		photos = Photo.filter_by(**filter_data)
		self.assertEqual(len(photos), 2)
		filter_data = {
			'photo': self.IMAGE_FILE()
		}
		photos = Photo.filter_by(**filter_data)
		self.assertEqual(len(photos), 1)
		filter_data = {
			'upload_time': 'time_1'
		}
		photos = Photo.filter_by(**filter_data)
		self.assertEqual(len(photos), 1)
	
	def test_get_by_id(self):
		self.assertEqual(Photo.get_by_id(100500), None)
		photo = Photo.get_by_id(self.id)
		self.assertEqual(photo.id, self.id)
		self.assertEqual(photo.owner, self.user)
		self.assertEqual(photo.photo, self.IMAGE_FILE('temp.png'))
		self.assertEqual(photo.upload_time, 'time')
	
	def test_get_all(self):
		photos = Photo.get_all()
		self.assertEqual(len(photos), 1)
		data = {
			'owner': self.user,
			'photo': self.IMAGE_FILE(),
			'upload_time': 'time_1'
		}
		photo_id = Photo.add(**data).id
		photos = Photo.get_all()
		self.assertEqual(len(photos), 2)
		Photo.get_by_id(self.id).delete()
		Photo.get_by_id(photo_id).delete()
		photos = Photo.get_all()
		self.assertEqual(len(photos), 0)
	
	def tearDown(self):
		try:
			os.remove('media/test.png')
		except OSError:
			pass
		try:
			os.remove('media/temp.png')
		except OSError:
			pass
		for file in glob.glob('media/test_*.png'):
			os.remove(file)
		for file in glob.glob('media/temp_*.png'):
			os.remove(file)
			
	@staticmethod
	def IMAGE_FILE(name='test.png'):
		img = ImageFile(open(name, 'w+'), name)
		os.remove(name)
		return img
