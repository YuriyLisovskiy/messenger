from django.shortcuts import render_to_response


def HttpForbidden(message: str):
	return render_to_response('chat/error.html', {
		'error_code': 403,
		'error_type': 'Forbidden',
		'error_message': message + ', access denied!'
	})


def HttpNotFound(message: str):
	return render_to_response('chat/error.html', {
		'error_code': 404,
		'error_type': 'Not found',
		'error_message': message + ' does not exist!'
	})
