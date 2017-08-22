def checkUsername(username):
    if len(username) > 2:
        return True
    return False

def checkEmail(email, userList):
    for ul in userList:
        if ul.email == email:
            return False
    return True

def checkPassword(password):
    if len(password) > 7:
        return True
    return False
