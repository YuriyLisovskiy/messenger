from django.conf.urls import url

from chat import views as dialog_views

appName = 'chat'

urlpatterns = [
	# Urls for accessing dialogs.
	url(r'^getDialogs/?$', dialog_views.GetDialogs.as_view(), name='get_dialogs'),
	url(r'^getDialog/?$', dialog_views.GetDialog.as_view(), name='get_dialog'),
	url(r'^createDialog/?$', dialog_views.CreateDialog.as_view(), name='create_dialog'),
	url(r'^deleteDialog/?$', dialog_views.DeleteDialog.as_view(), name='delete_dialog'),

	# Urls for accessing messages.
	url(r'^getMessages/?$', dialog_views.GetMessages.as_view(), name='get_messages'),
	url(r'^getMessage/?$', dialog_views.GetMessage.as_view(), name='get_message'),
	url(r'^sendMessage/?$', dialog_views.SendMessage.as_view(), name='send_message'),
	url(r'^updateMessage/?$', dialog_views.UpdateMessage.as_view(), name='update_message'),
	url(r'^deleteMessage/?$', dialog_views.DeleteMessage.as_view(), name='delete_message')
]
