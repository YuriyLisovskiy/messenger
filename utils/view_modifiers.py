from django.shortcuts import redirect

from .responses import PERMISSION_DENIED
from messenger.settings import LOGIN_REDIRECT_URL


def sudo_required(func):
	def wrapper(*args, **kwargs):
		request = None

		if 'request' in kwargs.keys():
			request = kwargs['request']
		elif 'request' in func.__code__.co_varnames:
			request_pos = func.__code__.co_varnames.index('request')
			request = args[request_pos]
		elif 'self' in func.__code__.co_varnames:
			if 'request' in vars(args[0]):
				request = func.__self__.request

		if request and not request.user.is_superuser:
			if not request.user.is_authenticated:
				return redirect(LOGIN_REDIRECT_URL)
			else:
				return PERMISSION_DENIED
		return func(*args, **kwargs)

	return wrapper


def auth_required(func):
	def wrapper(*args, **kwargs):
		request = None

		if 'request' in kwargs.keys():
			request = kwargs['request']
		elif 'request' in func.__code__.co_varnames:
			request_pos = func.__code__.co_varnames.index('request')
			request = args[request_pos]
		elif 'self' in func.__code__.co_varnames:
			if 'request' in vars(args[0]):
				request = func.__self__.request

		if request:
			if not request.user.is_authenticated:
				return redirect(LOGIN_REDIRECT_URL)
		return func(*args, **kwargs)

	return wrapper
