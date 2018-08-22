from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from account.models import UserProfile


# Represents dialog between two users.
class Dialog(models.Model):
	author = models.ForeignKey(UserProfile, null=True, related_name='author')
	friend = models.ForeignKey(UserProfile, null=True, related_name='friend')
	title = models.CharField(default="", max_length=256)
	last_message_id = models.IntegerField(default=0)
	logo = models.ImageField(blank=True)
	has_unread = models.BooleanField(default=True)
	link_id = models.IntegerField(default=0)
	
	@staticmethod
	def filter_by(pk=None, author=None, friend=None, has_unread=None):
		query = {}
		if pk and isinstance(pk, int):
			query['pk'] = pk
		if author and isinstance(author, UserProfile):
			query['author'] = author
		if friend and isinstance(friend, UserProfile):
			query['friend'] = friend
		if has_unread and isinstance(has_unread, bool):
			query['has_unread'] = has_unread
		return Dialog.objects.filter(**query)

	def to_dict(self):
		context = {
			'id': self.id,
			'title': self.title,
			'author_id': self.author.id,
			'friend_id': self.friend.id,
			'last_message_id': self.last_message_id,
			'has_unread': self.has_unread,
			'link_id': self.link_id
		}
		if self.logo:
			context['logo'] = self.logo.url
		return context
	
	@staticmethod
	def get_by_id(pk):
		if isinstance(pk, int):
			try:
				chat_room = Dialog.objects.get(pk=pk)
				return chat_room
			except ObjectDoesNotExist:
				return None
		return None

	@staticmethod
	def get_all():
		return Dialog.objects.all()
	
	@staticmethod
	def create(author, friend, logo, link_id, last_message_id=None):
		if not isinstance(author, UserProfile) or not isinstance(friend, UserProfile) or not isinstance(last_message_id, int) or not  isinstance(link_id, int):
			return None
		dialog = Dialog()
		dialog.title = friend.first_name + " " + friend.last_name
		dialog.author = author
		dialog.friend = friend
		dialog.logo = logo
		dialog.link_id = link_id
		if last_message_id:
			dialog.last_message_id = last_message_id
		return dialog
	
	def edit(self, author=None, friend=None, logo=None):
		if author and isinstance(author, UserProfile):
			self.author = author
		if friend and isinstance(friend, UserProfile):
			self.friend = friend
		if logo:
			self.logo = logo
		self.save()
	
	@staticmethod
	def remove(pk):
		if isinstance(pk, int):
			chat_room = Dialog.get_by_id(pk)
			if chat_room:
				chat_room.delete()
				return True
		return False


# Represents dialog message.
class Message(models.Model):
	dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, default=1)
	text = models.CharField(default="", max_length=9999999)
	time = models.CharField(default="", max_length=100)
	author_initials = models.CharField(default="", max_length=100)
	author_logo = models.FileField(blank=True)
	author_id = models.IntegerField(default=0)
	is_unread = models.BooleanField(default=True)
	link_id = models.IntegerField(default=0)

	def to_dict(self):
		context = {
			'id': self.id,
			'dialog_id': self.dialog.id,
			'text': self.text,
			'time': self.time,
			'author_fn_ln': self.author_initials,
			'author_id': self.author_id,
			'link_id': self.link_id
		}
		if self.author_logo:
			context['author_logo'] = self.author_logo.url
		return context

	@staticmethod
	def get_by_id(pk):
		if isinstance(pk, int):
			try:
				message = Message.objects.get(pk=pk)
				return message
			except ObjectDoesNotExist:
				return None
		return None
	
	@staticmethod
	def get_all():
		return Message.objects.all()
	
	@staticmethod
	def filter_by(pk=None, dialog=None, text=None, time=None, author_initials=None, author_logo=None, author_id=None, is_unread=None):
		query = {}
		if pk and isinstance(pk, int):
			query['pk'] = pk
		if dialog and isinstance(dialog, Dialog):
			query['dialog'] = dialog
		if text and isinstance(text, str):
			query['text'] = text
		if time and isinstance(time, str):
			query['time'] = time
		if author_initials and isinstance(author_initials, str):
			query['author_initials'] = author_initials
		if author_logo:
			query['author_logo'] = author_logo
		if author_id and isinstance(author_id, int):
			query['author_id'] = author_id
		if is_unread and isinstance(is_unread, bool):
			query['is_unread'] = is_unread
		return Message.objects.filter(**query)

	@staticmethod
	def create(dialog, text, author, time):
		if not isinstance(dialog, Dialog) or not isinstance(text, str) or not isinstance(author, UserProfile) or not isinstance(time, str):
			return None
		message = Message()
		message.dialog = dialog
		message.text = text
		message.author_username = author.username
		message.time = time
		message.author_initials = author.first_name[0] + author.last_name[0]
		message.author_logo = author.logo
		message.author_id = author.id
		return message
	
	def edit(self, dialog=None, text=None, author=None, time=None):
		if dialog and isinstance(dialog, Dialog):
			self.dialog = dialog
		if text and isinstance(text, str):
			self.text = text
		if author and isinstance(author, UserProfile):
			self.author_username = author.username
			self.author_initials = author.first_name[0] + author.last_name[0]
			self.author_logo = author.logo
			self.author_id = author.id
		if time and isinstance(time, str):
			self.time = time
		self.save()
	
	@staticmethod
	def remove(pk):
		if isinstance(pk, int):
			message = Message.get_by_id(pk)
			if message:
				message.delete()
				return True
		return False
