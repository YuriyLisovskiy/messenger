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
		self.img = self.IMAGE_FILE('test.png')
		data = {
			'author': self.user2,
			'friend': self.user1,
			'logo': self.img
		}
		self.ch_room_id = ChatRoom.add(**data).id
	
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
		chat_room = ChatRoom.get_by_id(self.ch_room_id)
		self.assertEqual(chat_room.author, self.user2)
		self.assertEqual(chat_room.friend, self.user1)
		self.assertEqual(chat_room.logo, self.img)
		img = self.IMAGE_FILE('temp.png')
		data = {
			'author': self.user1,
			'friend': self.user2,
			'logo': img
		}
		chat_room = ChatRoom.edit(100500, **data)
		self.assertEqual(chat_room, None)
		ChatRoom.edit(self.ch_room_id, **data)
		chat_room = ChatRoom.get_by_id(self.ch_room_id)
		self.assertNotEqual(chat_room.author, self.user2)
		self.assertNotEqual(chat_room.friend, self.user1)
		self.assertNotEqual(chat_room.logo, self.img)
		self.assertEqual(chat_room.author, self.user1)
		self.assertEqual(chat_room.friend, self.user2)
		self.assertEqual(chat_room.logo, img)
	
	def test_get_by_id(self):
		chat_room = ChatRoom.get_by_id(100500)
		self.assertEqual(chat_room, None)
		chat_room = ChatRoom.get_by_id(self.ch_room_id)
		self.assertEqual(chat_room.author, self.user2)
		self.assertEqual(chat_room.friend, self.user1)
		self.assertEqual(chat_room.logo, self.img)
		
	def test_get_all(self):
		chat_rooms = ChatRoom.get_all()
		self.assertEqual(len(chat_rooms), 1)
		data = {
			'author': self.user1,
			'friend': self.user2,
			'logo': self.IMAGE_FILE('temp.png')
		}
		ch_r_id = ChatRoom.add(**data).id
		chat_rooms = ChatRoom.get_all()
		self.assertEqual(len(chat_rooms), 2)
		ChatRoom.remove(ch_r_id)
		ChatRoom.remove(self.ch_room_id)
		chat_rooms = ChatRoom.get_all()
		self.assertEqual(len(chat_rooms), 0)
		
	def test_remove(self):
		ChatRoom.remove(100500)
		ChatRoom.remove(self.ch_room_id)
		chat_room = ChatRoom.get_by_id(self.ch_room_id)
		self.assertEqual(chat_room, None)
		
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
