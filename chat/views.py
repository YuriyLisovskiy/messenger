from datetime import datetime

from django.http import JsonResponse
from django.views.generic import View

from account.models import UserProfile
from chat.models import Message, Dialog
from utils.view_modifiers import auth_required
from utils.responses import NOT_FOUND, BAD_REQUEST, OK, CREATED


# Returns all dialogs in json format for current user.
#
# API url: /api/v1/dialogs/getDialogs
class GetDialogs(View):

	@auth_required
	def get(self, request):
		author = UserProfile.get_by_id(request.user.pk)
		response = {
			'data': {
				'chats': [x.to_dict() for x in Dialog.filter_by(author=author)]
			},
			'status': "OK"
		}
		return JsonResponse(response, status=200, safe=False)

	@staticmethod
	def post():
		return BAD_REQUEST


# Returns dialog in json format.
#
# API url: /api/v1/dialogs/getDialog
# Required params:
#   - 'id': int
class GetDialog(View):

	@auth_required
	def get(self, request):
		if 'id' in request.GET:
			dialog_id = request.GET.get('id')
			if isinstance(dialog_id, int):
				filter_data = {
					'author': UserProfile.get_by_id(request.user.pk),
					'id': dialog_id
				}
				dialog = Dialog.filter_by(**filter_data).first()
				if dialog:
					response = {
						'data': dialog.to_dict(),
						'status': "OK"
					}
					return JsonResponse(response, status=200, safe=False)
				return NOT_FOUND
		return BAD_REQUEST

	@staticmethod
	def post():
		return BAD_REQUEST


# Creates dialog.
#
# API url: /api/v1/dialogs/createDialog
# Required params:
#   - 'companion_id': int
class CreateDialog(View):
	
	@staticmethod
	def get():
		return BAD_REQUEST
	
	@auth_required
	def post(self, request):
		if 'companion_id' in request.POST:
			author = UserProfile.get_by_id(request.user.pk)
			friend = UserProfile.get_by_id(request.POST.get('companion_id'))
			if not author or not friend:
				return NOT_FOUND
			filter_data = {
				'author': author,
				'friend': friend
			}
			initial_dialog = Dialog.filter_by(**filter_data).first()
			if not initial_dialog:
				dialog_data = {
					'author': author,
					'friend': friend,
					'logo': friend.user_logo
				}
				initial_dialog = Dialog.create(**dialog_data)
			filter_data = {
				'author': friend,
				'friend': author
			}
			secondary_dialog = Dialog.filter_by(**filter_data)
			if not secondary_dialog:
				dialog_data = {
					'author': friend,
					'friend': author,
					'logo': author.user_logo
				}
				secondary_dialog = Dialog.create(**dialog_data)
			initial_dialog.link_id = secondary_dialog.id
			secondary_dialog.link_id = initial_dialog.id
			initial_dialog.save()
			secondary_dialog.save()
			return CREATED
		return BAD_REQUEST


# Removes dialog.
#
# API url: /api/v1/dialogs/deleteDialog
# Required params:
#   - 'id': int
class DeleteDialog(View):

	@staticmethod
	def get():
		return BAD_REQUEST

	@auth_required
	def post(self, request):
		if 'id' in request.POST:
			dialog = None
			dialog_id = request.POST.get('id')
			if isinstance(dialog, int):
				filter_data = {
					'author': UserProfile.get_by_id(request.user.id),
					'pk': dialog_id
				}
				dialog = Dialog.filter_by(**filter_data).first()
			if dialog:
				if dialog.id != dialog.link_id:
					secondary_dialog = Dialog.filter_by(pk=dialog.link_id).first()
					if secondary_dialog:
						secondary_dialog.link_id = secondary_dialog.id
						secondary_dialog.save()
				if Dialog.remove(dialog.id):
					return CREATED
			return NOT_FOUND
		return BAD_REQUEST


# Returns messages from given dialog.
#
# API url: /api/v1/dialogs/getMessages
# Required params:
#   - 'dialog_id': int
class GetMessages(View):

	@auth_required
	def get(self, request):
		if 'dialog_id' in request.GET:
			filter_data = {
				'author': UserProfile.get_by_id(request.user.pk),
				'id': request.GET.get('dialog_id')
			}
			dialog = Dialog.filter_by(**filter_data).first()
			if dialog:
				messages = Message.filter_by(dialog=dialog)
				offset = len(messages)
				if 'offset' in request.GET:
					if isinstance(offset, int):
						offset = int(request.GET.get('offset'))
				if offset <= len(messages):
					messages = messages[len(messages) - offset:]
				else:
					return BAD_REQUEST
				response = {
					'data': {
						'messages': [message.to_dict() for message in messages]
					},
					'status': 'OK'
				}
				return JsonResponse(response, status=200, safe=False)
			return NOT_FOUND
		return BAD_REQUEST

	@staticmethod
	def post():
		return BAD_REQUEST


# Returns message from given dialog.
#
# API url: /api/v1/dialogs/getMessage
# Required params:
#   - 'dialog_id': int
#   - 'message_id': int
class GetMessage(View):

	@auth_required
	def get(self, request):
		if 'dialog_id' in request.GET and 'message_id' in request.GET:
			filter_data = {
				'author': UserProfile.get_by_id(request.user.pk),
				'dialog_id': request.GET.get('dialog_id'),
			}
			dialog = Dialog.filter_by(**filter_data).first()
			if dialog:
				message = Message.filter_by(dialog=dialog, pk=request.GET.get('message_id'))
				if message:
					response = {
						'data': {
							message.to_dict()
						},
						'status': 'OK'
					}
					return JsonResponse(response, status=200, safe=False)
			return NOT_FOUND
		return BAD_REQUEST

	@staticmethod
	def post():
		return BAD_REQUEST


# Sends message from given dialog.
#
# API url: /api/v1/dialogs/sendMessage
# Required params:
#   - 'dialog_id': int
#   - 'message_id': int
class SendMessage(View):

	@staticmethod
	def get():
		return BAD_REQUEST

	@auth_required
	def post(self, request):
		if 'text' in request.POST and 'companion_id' in request.POST:
			text = request.POST.get('text')
			if text != '':
				author = UserProfile.get_by_id(request.user.pk)
				friend = UserProfile.get_by_id(request.POST.get('companion_id'))
				if not author or not friend:
					return NOT_FOUND
				filter_data = {
					'author': author,
					'friend': friend
				}
				dialog = Dialog.filter_by(**filter_data).first()
				if not dialog:
					return NOT_FOUND
				msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + str(
					datetime.now().strftime("%d %b %Y"))[:11]
				message_data = {
					'chat_room': dialog,
					'author': author,
					'text': text,
					'time': msg_time,
				}
				initial_message = Message.create(**message_data)
				initial_message.link_id = initial_message.id
				if author != friend:
					filter_data = {
						'author': friend,
						'friend': author
					}
					dialog = Dialog.filter_by(**filter_data).first()
					if dialog:
						message_data = {
							'chat_room': dialog,
							'author': author,
							'text': text,
							'time': msg_time,
							'link_id': initial_message.id
						}
						secondary_message = Message.create(**message_data)
						initial_message.link_id = secondary_message.id
						secondary_message.link_id = initial_message.id
						secondary_message.save()
					else:
						return NOT_FOUND
				initial_message.save()
				return OK
		return BAD_REQUEST


# Updates message from given dialog.
#
# API url: /api/v1/dialogs/updateMessage
# Required params:
#   - 'dialog_id': int
#   - 'message_id': int
class UpdateMessage(View):

	@staticmethod
	def get():
		return BAD_REQUEST

	@auth_required
	def post(self, request):
		if 'dialog_id' in request.POST and 'message_id' in request.POST and 'text' in request.POST:
			initial_dialog = Dialog.filter_by(pk=request.POST.get('dialog_id'), author=UserProfile.get_by_id(request.user.id)).first()
			if initial_dialog:
				initial_message = Message.filter_by(pk=request.POST.get('message_id'), dialog=initial_dialog).first()
				if initial_message:
					initial_message.edit(text=request.POST.get('text'))
					if initial_dialog.id != initial_dialog.link_id:
						secondary_dialog = Dialog.filter_by(pk=initial_dialog.link_id).first()
						if not secondary_dialog:
							return NOT_FOUND
						secondary_message = Message.filter_by(pk=initial_message.link_id, dialog=secondary_dialog).first()
						if secondary_message:
							secondary_message.edit(text=request.POST.get('text'))
					return CREATED
			return NOT_FOUND
		return BAD_REQUEST


# Deletes message from given dialog.
#
# API url: /api/v1/dialogs/deleteMessage
# Required params:
#   - 'dialog_id': int
#   - 'message_id': int
#   - 'delete_both': bool
class DeleteMessage(View):

	@staticmethod
	def get():
		return BAD_REQUEST
	
	@auth_required
	def post(self, request):
		if 'dialog_id' in request.POST and 'message_id' in request.POST:
			initial_dialog = Dialog.filter_by(pk=request.POST.get('dialog_id'), author=UserProfile.get_by_id(request.user.id)).first()
			if initial_dialog:
				initial_message = Message.filter_by(pk=request.POST.get('message_id'), dialog=initial_dialog).first()
				if initial_message:
					if request.POST.get('delete_both'):
						if initial_dialog.id != initial_dialog.link_id:
							secondary_dialog = Dialog.filter_by(pk=initial_dialog.link_id).first()
							if not secondary_dialog:
								return NOT_FOUND
							secondary_message = Message.filter_by(pk=initial_message.link_id, dialog=secondary_dialog).first()
							if secondary_message:
								Message.remove(secondary_message.id)
					Message.remove(initial_message.id)
					return CREATED
			return NOT_FOUND
		return BAD_REQUEST
