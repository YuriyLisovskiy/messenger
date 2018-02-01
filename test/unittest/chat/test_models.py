import os
import glob

from django.test import TestCase
from django.core.files.images import ImageFile
from django.utils.datetime_safe import datetime

from account.models import UserProfile
from chat.models import Message, ChatRoom


class TestChatRoom(TestCase):

	def setUp(self):
		data = {
			'first_name': 'some_first_name',
			'last_name': 'some_last_name',
			'username': 'some_username',
			'email': 'some.email@gmail.com',
			'password': 'super_safe_password',
		}
		self.user1 = UserProfile.add(**data)
		data = {
			'first_name': 'another_first_name',
			'last_name': 'another_last_name',
			'username': 'another_username',
			'email': 'another.email@gmail.com',
			'password': 'super_safe_password',
		}
		self.user2 = UserProfile.add(**data)
	
	def test_add(self):
		img = self.IMAGE_FILE('temp.png')
		data = {
			'author': self.user1,
			'friend': self.user2,
			'logo': img
		}
		ch_room_id = ChatRoom.add(**data).id
		chat_room = ChatRoom.get_by_id(ch_room_id)
		self.assertEqual(chat_room.author, self.user1)
		self.assertEqual(chat_room.friend, self.user2)
		self.assertEqual(chat_room.logo, img)
	
	def test_edit(self):
		pass
	
	def test_get_by_id(self):
		pass
	
	def test_filter_by(self):
		pass
	
	def test_get_all(self):
		pass
	
	def test_remove(self):
		pass
	
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


class TestMessage(TestCase):
	pass
