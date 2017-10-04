from chat.models import Message, ChatRoom


def checkUsername(username: str):
    if len(username) > 2:
        return True
    return False


def checkEmail(email, userList):
    for ul in userList:
        if ul.email == email:
            return False
    return True


def checkPassword(password: str):
    if len(password) > 7:
        return True
    return False


def create_chat_room(room_data: dict):
    return ChatRoom.objects.create(
        author=room_data['author'],
        friend=room_data['friend'],
        author_id=room_data['author_id'],
        friend_id=room_data['friend_id'],
        logo=room_data['logo']
    )


def create_message(message_data: dict):
    Message.objects.create(
        chat_room=message_data['chat_room'],
        msg=message_data['message'],
        time=message_data['message_time'],
        author=message_data['author_username'],
        author_fn_ln=message_data['author_initials'],
        author_logo=message_data['author_logo'],
        author_id=message_data['author_id']
    )
