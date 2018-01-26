from django.test import TestCase

from account.models import UserProfile
from utils.helpers import password_is_valid, email_does_not_exist, username_is_valid


class TestHelpers(TestCase):
	def setUp(self):
		data = {
			'first_name': 'test_first_name_1',
			'last_name': 'test_last_name_1',
			'username': 'some_username_1',
			'email': 'test_email@gmail.com',
			'password': 'super_safe_password_1'
		}
		UserProfile.add(**data)
		data = {
			'first_name': 'test_first_name_2',
			'last_name': 'test_last_name_2',
			'username': 'some_username_2',
			'email': 'test_email@gmail.com',
			'password': 'super_safe_password_2'
		}
		UserProfile.add(**data)
	
	def test_password_is_valid(self):
		self.assertEqual(password_is_valid('123456qwerty'), True)
		self.assertEqual(password_is_valid('12345'), False)
	
	def test_email_exists(self):
		self.assertEqual(email_does_not_exist('test_email@gmail.com', UserProfile.get_all()), False)
		self.assertEqual(email_does_not_exist('some_other_email@gmail.com', UserProfile.get_all()), True)
	
	def test_username_is_valid(self):
		self.assertEqual(username_is_valid('some_username_1'), True)
		self.assertEqual(username_is_valid('su'), False)
