from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from account.models import UserProfile


class ChatRoom(models.Model):
	author = models.ForeignKey(UserProfile, null=True, related_name='author')
	friend = models.ForeignKey(UserProfile, null=True, related_name='friend')
	title = models.CharField(default="", max_length=256)
	last_message_id = models.IntegerField(default=0)
	logo = models.ImageField(blank=True)
	has_unread = models.BooleanField(default=True)
	
	@staticmethod
	def filter_by(author=None, friend=None, **kwargs):
		query = {}
		if author:
			query['author'] = author
		if friend:
			query['friend'] = friend
		query.update(**kwargs)
		return ChatRoom.objects.filter(**query)
	
	def to_dict(self):
		context = {
			'id': self.id,
			'title': self.title,
			'author_id': self.author.id,
			'friend_id': self.friend.id,
			'last_message_id': self.last_message_id,
			'has_unread': self.has_unread
		}
		if self.logo:
			context['logo'] = self.logo.url
		return context
	
	@staticmethod
	def get_by_id(pk):
		try:
			chat_room = ChatRoom.objects.get(pk=pk)
			return chat_room
		except ObjectDoesNotExist:
			return None
	
	@staticmethod
	def get_all():
		return ChatRoom.objects.all()
	
	@staticmethod
	def add(author, friend, logo, last_message_id=None):
		chat_room = ChatRoom()
		chat_room.title = friend.first_name + " " + friend.last_name
		chat_room.author = author
		chat_room.friend = friend
		chat_room.logo = logo
		if last_message_id:
			chat_room.last_message_id = last_message_id
		chat_room.save()
		return chat_room
	
	@staticmethod
	def edit(pk, author=None, friend=None, logo=None):
		chat_room = ChatRoom.get_by_id(pk)
		if not chat_room:
			return None
		if author:
			chat_room.author = author
		if friend:
			chat_room.friend = friend
		if logo:
			chat_room.logo = logo
		chat_room.save()
		return chat_room
	
	@staticmethod
	def remove(pk):
		chat_room = ChatRoom.get_by_id(pk)
		if chat_room:
			chat_room.delete()
			return True
		return False


class Message(models.Model):
	chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, default=1)
	msg = models.CharField(default="", max_length=9999999)
	time = models.CharField(default="", max_length=100)
	author_initials = models.CharField(default="", max_length=100)
	author_logo = models.FileField(blank=True)
	author_id = models.IntegerField(default=0)
	is_unread = models.BooleanField(default=True)

	def to_dict(self):
		context = {
			'id': self.id,
			'chat_id': self.chat_room.id,
			'message': self.msg,
			'time': self.time,
			'author_fn_ln': self.author_initials,
			'author_id': self.author_id
		}
		if self.author_logo:
			context['author_logo'] = self.author_logo.url
		return context

	@staticmethod
	def get_by_id(pk):
		try:
			message = Message.objects.get(pk=pk)
			return message
		except ObjectDoesNotExist:
			return None
	
	@staticmethod
	def get_all():
		return Message.objects.all()
	
	@staticmethod
	def filter_by(chat_room=None, msg=None, author=None, time=None, author_initials=None, author_logo=None,
				author_id=None, **kwargs):
		query = {}
		if chat_room:
			query['chat_room'] = chat_room
		if msg:
			query['msg'] = msg
		if author:
			query['author_username'] = author.username
		if time:
			query['time'] = time
		if author_initials:
			query['author_initials'] = author_initials
		if author_logo:
			query['author_logo'] = author_logo
		if author_id:
			query['author_id'] = author_id
		query.update(**kwargs)
		return Message.objects.filter(**query)
		
	@staticmethod
	def add(chat_room, msg, author, time):
		message = Message()
		message.chat_room = chat_room
		message.msg = msg
		message.author_username = author.username
		message.time = time
		message.author_initials = author.first_name[0] + author.last_name[0]
		message.author_logo = author.logo
		message.author_id = author.id
		message.save()
		return message
	
	@staticmethod
	def edit(pk, chat_room=None, msg=None, author=None, time=None):
		message = Message.get_by_id(pk)
		if not message:
			return None
		if chat_room:
			message.chat_room = chat_room
		if msg:
			message.msg = msg
		if author:
			message.author_username = author.username
			message.author_initials = author.first_name[0] + author.last_name[0]
			message.author_logo = author.logo
			message.author_id = author.id
		if time:
			message.time = time
		message.save()
		return message
	
	@staticmethod
	def remove(pk):
		message = Message.get_by_id(pk)
		if message:
			message.delete()
			return True
		return False
