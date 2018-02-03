import os
import glob

from django.test import TestCase
from django.core.files.images import ImageFile

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
	
	def setUp(self):
		data = {
			'first_name': 'some_first_name',
			'last_name': 'some_last_name',
			'username': 'some_username',
			'email': 'some.email@gmail.com',
			'password': 'super_safe_password',
		}
		self.user1 = UserProfile.add(**data)
		self.user1.logo = self.IMAGE_FILE()
		self.user1.save()
		data = {
			'first_name': 'another_first_name',
			'last_name': 'another_last_name',
			'username': 'another_username',
			'email': 'another.email@gmail.com',
			'password': 'super_safe_password',
			'logo': self.IMAGE_FILE('temp.png')
		}
		self.user2 = UserProfile.add(**data)
		self.user2.logo = self.IMAGE_FILE('test.png')
		self.user2.save()
		data = {
			'author': self.user2,
			'friend': self.user1,
			'logo': self.user2.logo
		}
		self.ch_room = ChatRoom.add(**data)
		message_data = {
			'chat_room': self.ch_room,
			'author': self.user2,
			'msg': 'Some message text',
			'time': 'some time'
		}
		self.msg_id = Message.add(**message_data).id
	
	def test_add(self):
		message_data = {
			'chat_room': self.ch_room,
			'author': self.user1,
			'msg': 'Some message',
			'time': 'time',
		}
		msg_id = Message.add(**message_data).id
		message = Message.get_by_id(msg_id)
		self.assertEqual(message.chat_room, self.ch_room)
		self.assertEqual(message.msg, 'Some message')
		self.assertEqual(message.author_username, self.user1.username)
		self.assertEqual(message.time, 'time')
		self.assertEqual(message.author_fn_ln, self.user1.first_name[0] + self.user1.last_name[0])
		self.assertEqual(message.author_logo, self.user1.logo)
		self.assertEqual(message.author_id, str(self.user1.id))
	
	def test_edit(self):
		message = Message.get_by_id(self.msg_id)
		self.assertEqual(message.chat_room, self.ch_room)
		self.assertEqual(message.msg, 'Some message text')
		self.assertEqual(message.author_username, self.user2.username)
		self.assertEqual(message.time, 'some time')
		self.assertEqual(message.author_fn_ln, self.user2.first_name[0] + self.user2.last_name[0])
		self.assertEqual(message.author_logo, self.user2.logo)
		self.assertEqual(message.author_id, str(self.user2.id))
		message_data = {
			'chat_room': self.ch_room,
			'author': self.user1,
			'msg': 'Some message',
			'time': 'time',
		}
		message = Message.edit(pk=100500, **message_data)
		self.assertEqual(message, None)
		Message.edit(pk=self.msg_id, **message_data)
		message = Message.get_by_id(self.msg_id)
		self.assertEqual(message.chat_room, self.ch_room)
		self.assertEqual(message.msg, 'Some message')
		self.assertEqual(message.author_username, self.user1.username)
		self.assertEqual(message.time, 'time')
		self.assertEqual(message.author_fn_ln, self.user1.first_name[0] + self.user1.last_name[0])
		self.assertEqual(message.author_logo, self.user1.logo)
		self.assertEqual(message.author_id, str(self.user1.id))
	
	def test_filter_by(self):
		message_data = {
			'chat_room': self.ch_room,
			'author': self.user1,
			'msg': 'Message text',
			'time': 'some time',
		}
		Message.add(**message_data)
		filter_data = {
			'chat_room': self.ch_room
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 2)
		filter_data = {
			'msg': 'Message text'
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 1)
		filter_data = {
			'author': self.user1
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 1)
		filter_data = {
			'time': 'some time'
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 2)
		filter_data = {
			'author_fn_ln': self.user1.first_name[0] + self.user1.last_name[0]
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 1)
		filter_data = {
			'author_logo': self.user1.logo
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 1)
		filter_data = {
			'author_id': self.user2.id
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 1)
		filter_data = {
			'time': 'interesting time'
		}
		messages = Message.filter_by(**filter_data)
		self.assertEqual(len(messages), 0)
	
	def test_get_all(self):
		messages = Message.get_all()
		self.assertEqual(len(messages), 1)
		message_data = {
			'chat_room': self.ch_room,
			'author': self.user1,
			'msg': 'Some message',
			'time': 'time',
		}
		msg_id = Message.add(**message_data).id
		messages = Message.get_all()
		self.assertEqual(len(messages), 2)
		Message.remove(msg_id)
		Message.remove(self.msg_id)
		messages = Message.get_all()
		self.assertEqual(len(messages), 0)
	
	def test_to_dict(self):
		message = Message.get_by_id(self.msg_id)
		message_dict = message.to_dict()
		self.assertEqual(message_dict['id'], self.msg_id)
		self.assertEqual(message_dict['chat_room'], self.ch_room.id)
		self.assertEqual(message_dict['msg'], 'Some message text')
		self.assertEqual(message_dict['author_username'], self.user2.username)
		self.assertEqual(message_dict['time'], 'some time')
		self.assertEqual(message_dict['author_fn_ln'], self.user2.first_name[0] + self.user2.last_name[0])
		self.assertEqual(message_dict['author_id'], str(self.user2.id))
		self.assertEqual(message_dict['author_logo'], self.user2.logo.url)
	
	def test_remove(self):
		Message.remove(self.msg_id)
		message = Message.get_by_id(self.msg_id)
		self.assertEqual(message, None)
		Message.remove(100500)
	
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
