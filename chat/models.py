from django.db import models
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

from account.models import UserProfile


class ChatRoom(models.Model):
	author = models.ForeignKey(UserProfile, null=True, related_name='author')
	friend = models.ForeignKey(UserProfile, null=True, related_name='friend')
	logo = models.ImageField(blank=True)
	
	@staticmethod
	def filter_by(author=None, friend=None, logo=None, **kwargs):
		query = {}
		if author:
			query['author'] = author
		if friend:
			query['friend'] = friend
		if logo:
			query['logo'] = logo
		query.update(**kwargs)
		try:
			chat_rooms = ChatRoom.objects.filter(**query)
			return chat_rooms
		except EmptyResultSet:
			return None
	
	@staticmethod
	def get_by_id(pk):
		try:
			chat_room = ChatRoom.objects.get(pk=pk)
			return chat_room
		except ObjectDoesNotExist:
			return None
	
	@staticmethod
	def get_all():
		try:
			chat_rooms = ChatRoom.objects.all()
			return chat_rooms
		except EmptyResultSet:
			return None
	
	@staticmethod
	def add(author, friend, logo, **kwargs):
		chat_room = ChatRoom.filter_by(author=author, friend=friend, logo=logo).first()
		if not chat_room:
			chat_room = ChatRoom()
			chat_room.author = author
			chat_room.friend = friend
			chat_room.logo = logo
			chat_room.save()
		return chat_room
	
	@staticmethod
	def edit(pk, author=None, friend=None, logo=None, **kwargs):
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
	msg = models.CharField(default="", max_length=99999)
	author_username = models.CharField(default="", max_length=100)
	time = models.CharField(default="", max_length=100)
	author_fn_ln = models.CharField(default="", max_length=100)
	author_logo = models.FileField(blank=True)
	author_id = models.CharField(default="", max_length=100)

	def to_dict(self):
		context = {
			'id': self.id,
			'chat_room': self.chat_room.id,
			'msg': self.msg,
			'author_username': self.author_username,
			'time': self.time,
			'author_fn_ln': self.author_fn_ln,
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
		try:
			messages = Message.objects.all()
			return messages
		except EmptyResultSet:
			return None
	
	@staticmethod
	def filter_by(chat_room=None, msg=None, author=None, time=None, author_fn_ln=None, author_logo=None,
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
		if author_fn_ln:
			query['author_fn_ln'] = author_fn_ln
		if author_logo:
			query['author_logo'] = author_logo
		if author_id:
			query['author_id'] = author_id
		query.update(**kwargs)
		try:
			messages = Message.objects.filter(**query)
			return messages
		except EmptyResultSet:
			return None
	
	@staticmethod
	def add(chat_room, msg, author, time, **kwargs):
		message = Message()
		message.chat_room = chat_room
		message.msg = msg
		message.author_username = author.username
		message.time = time
		message.author_fn_ln = author.first_name[0] + author.last_name[0]
		message.author_logo = author.logo
		message.author_id = author.id
		message.save()
		return message
	
	@staticmethod
	def edit(pk, chat_room=None, msg=None, author=None, time=None, **kwargs):
		message = Message.get_by_id(pk)
		if not message:
			return None
		if chat_room:
			message.chat_room = chat_room
		if msg:
			message.msg = msg
		if author:
			message.author_username = author.username
			message.author_fn_ln = author.first_name[0] + author.last_name[0]
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
