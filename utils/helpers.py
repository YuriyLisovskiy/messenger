def username_is_valid(username: str):
	if len(username) > 2:
		return True
	return False


def email_does_not_exist(email, users):
	if not users:
		return True
	for usr in users:
		if usr.email == email:
			return False
	return True


def password_is_valid(password: str):
	if len(password) > 7:
		return True
	return False
