from django.http import HttpResponse
from django.shortcuts import render_to_response

OK = HttpResponse('ok', status=200)
CREATED = HttpResponse('created', status=201)


def BAD_REQUEST():
	return render_to_response('error.html', {
		'error_code': 400,
		'error_type': 'Bad request',
		'error_message': 'Bad request'
	})


def PERMISSION_DENIED():
	return render_to_response('error.html', {
		'error_code': 403,
		'error_type': 'Forbidden',
		'error_message': 'Access denied'
	})


def NOT_FOUND():
	return render_to_response('error.html', {
		'error_code': 404,
		'error_type': 'Not found',
		'error_message': 'The web page does not exist'
	})
