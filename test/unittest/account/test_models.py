import os

from django.test import TestCase
from django.core.files.images import ImageFile
from django.utils.datetime_safe import datetime

from account.models import UserProfile, PhotoLogo


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
		file = open('test.png', 'w+')
		user.logo = ImageFile(file, 'test.png')
		os.remove('test.png')
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

'''
class TestPhotoLogo(TestCase):
	
	def setUp(self):
		pass
	
	def test_add(self):
		pass
	
	def test_edit(self):
		pass
	
	def test_filter_by(self):
		pass
	
	def test_get_by_id(self):
		pass
	
	def test_get_all(self):
		pass
'''
