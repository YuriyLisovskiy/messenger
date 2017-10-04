from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, UserProfile
from django.http import JsonResponse
from .models import Message, PhotoLogo, ChatRoom
from .serializers import MessageSerializer, UserSerializer
from datetime import datetime
from utils import functions, response, header
import smtplib
from email.mime.text import MIMEText
from rest_framework.views import APIView
from messenger.settings import *


def index(request):
    return render(request, "chat/index.html")


def chat(request):
    if not request.user.is_authenticated:
        return response.HttpForbidden('You are not authenticated')
    user = request.user
    all_users = UserProfile.objects.all()
    all_chat_rooms = ChatRoom.objects.all()
    return render(request, "chat/chat.html", {
        'user': user,
	    'all_users': all_users,
        'all_chat_rooms': all_chat_rooms
    })


class Profile(View):

    def get(self, request, profile_id):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        try:
            user_profile = UserProfile.objects.get(pk=profile_id)
        except UserProfile.DoesNotExist:
            return response.HttpNotFound('User')
        if user_profile.user_country != '':
            user_profile.user_country = header.CountryList().get_county(user_profile.user_country)
        user_logos = PhotoLogo.objects.filter(owner__username=user_profile.username)
        return render(request, "chat/user_profile.html", {
            'user_profile': user_profile,
            'user_logos': user_logos,
        })

    def post(self, request, profile_id):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        if 'message' in request.POST:
            author_id, friend_id = request.POST['data'].split()
            msg = request.POST['message']
            try:
                author = UserProfile.objects.get(id=author_id)
                friend = UserProfile.objects.get(id=friend_id)
            except UserProfile.DoesNotExist:
                return response.HttpNotFound('User')
            author_initials = author.first_name[0] + author.last_name[0]
            msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + datetime.now().strftime("%d %b %Y")[:11]
            try:
                author_chat_room = ChatRoom.objects.get(
                    friend__id=friend_id,
                    author__id=author_id
                )
            except ChatRoom.DoesNotExist:
                author_chat_room = None
            try:
                friend_chat_room = ChatRoom.objects.get(
                    friend__id=author_id,
                    author__id=friend_id
                )
            except ChatRoom.DoesNotExist:
                friend_chat_room = None
            if not author_chat_room and not friend_chat_room:
                if author == friend:
                    room_data = {
                        'author': author,
                        'friend': author,
                        'author_id': author_id,
                        'friend_id': author_id,
                        'logo': author.user_logo
                    }
                    chat_room = functions.create_chat_room(room_data)
                    if msg != "":
                        message_data = {
                            'chat_room': chat_room,
                            'message': msg,
                            'message_time': msg_time,
                            'author_username': author.username,
                            'author_initials': author_initials,
                            'author_logo': author.user_logo,
                            'author_id': author_id
                        }
                        functions.create_message(message_data)
                    return redirect('/user/' + str(request.user.id))
                room_data = {
                    'author': author,
                    'friend': friend,
                    'author_id': author_id,
                    'friend_id': friend_id,
                    'logo': friend.user_logo
                }
                chat_room = functions.create_chat_room(room_data)
                if msg != "":
                    message_data = {
                        'chat_room': chat_room,
                        'message': msg,
                        'message_time': msg_time,
                        'author_username': author.username,
                        'author_initials': author_initials,
                        'author_logo': author.user_logo,
                        'author_id': author_id
                    }
                    functions.create_message(message_data)
                room_data = {
                    'author': friend,
                    'friend': author,
                    'author_id': friend_id,
                    'friend_id': author_id,
                    'logo': author.user_logo
                }
                chat_room = functions.create_chat_room(room_data)
                if msg != "":
                    message_data = {
                        'chat_room': chat_room,
                        'message': msg,
                        'message_time': msg_time,
                        'author_username': author.username,
                        'author_initials': author_initials,
                        'author_logo': author.user_logo,
                        'author_id': author_id
                    }
                    functions.create_message(message_data)
                    return redirect('/user/' + str(request.user.id))
            if msg != "":
                if author_chat_room:
                    message_data = {
                        'chat_room': author_chat_room,
                        'message': msg,
                        'message_time': msg_time,
                        'author_username': author.username,
                        'author_initials': author_initials,
                        'author_logo': author.user_logo,
                        'author_id': author_id
                    }
                    functions.create_message(message_data)
                    if not friend_chat_room:
                        room_data = {
                            'author': friend,
                            'friend': author,
                            'author_id': friend_id,
                            'friend_id': author_id,
                            'logo': author.user_logo
                        }
                        chat_room = functions.create_chat_room(room_data)
                        message_data = {
                            'chat_room': chat_room,
                            'message': msg,
                            'message_time': msg_time,
                            'author_username': author.username,
                            'author_initials': author_initials,
                            'author_logo': author.user_logo,
                            'author_id': author_id
                        }
                        functions.create_message(message_data)
                if friend_chat_room:
                    if author_chat_room != friend_chat_room:
                        message_data = {
                            'chat_room': friend_chat_room,
                            'message': msg,
                            'message_time': msg_time,
                            'author_username': author.username,
                            'author_initials': author_initials,
                            'author_logo': author.user_logo,
                            'author_id': author_id
                        }
                        functions.create_message(message_data)
                        if not author_chat_room:
                            room_data = {
                                'author': author,
                                'friend': friend,
                                'author_id': author_id,
                                'friend_id': friend_id,
                                'logo': friend.user_logo
                            }
                            chat_room = functions.create_chat_room(room_data)
                            message_data = {
                                'chat_room': chat_room,
                                'message': msg,
                                'message_time': msg_time,
                                'author_username': author.username,
                                'author_initials': author_initials,
                                'author_logo': author.user_logo,
                                'author_id': author_id
                            }
                            functions.create_message(message_data)
                    return redirect('/user/' + str(request.user.id))
                return redirect('/user/' + str(request.user.id))
            return redirect('/user/' + str(request.user.id))
        else:
            try:
                user_profile = UserProfile.objects.get(id=request.user.id)
            except UserProfile.DoesNotExist:
                return response.HttpNotFound('User')
            upload_time = str(datetime.now())[11:16] + "  |  " + str(datetime.now().strftime("%d %b %Y"))[:11]
            if 'logo' in request.FILES:
                request_logo = request.FILES['logo']
                user_profile.user_logo = request_logo
                try:
                    chat_rooms = ChatRoom.objects.filter(friend=user_profile)
                    for room in chat_rooms:
                        room.logo = request_logo
                        room.save()
                except ChatRoom.DoesNotExist:
                    pass
                try:
                    messages = Message.objects.filter(author_id=user_profile.id)
                    for message in messages:
                        message.author_logo = request_logo
                        message.save()
                except Message.DoesNotExist:
                    pass
                PhotoLogo.objects.create(
                    owner=user_profile,
                    photo=request_logo,
                    upload_time=upload_time
                )
            user_profile.save()
            return redirect('/user/' + str(request.user.id))


class SearchPeople(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        data = UserProfile.objects.all()
        return render(request, "chat/search.html", {'all_users': data})

    def post(self, request):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        keyword = request.POST['search']
        if 'city' in request.POST:
            f_n, l_n = keyword.split()
            birthday = request.POST['birthday']
            data = UserProfile.objects.filter(
                first_name=f_n,
                last_name=l_n,
                user_city=request.POST['city'],
                user_country=request.POST['country'],
                user_birthday_day=birthday[8:],
                user_birthday_month=birthday[5:7],
                user_birthday_year=birthday[:4],
                user_gender=request.POST['gender']
            )
        elif " " in keyword:
            f_n, l_n = keyword.split()
            data = UserProfile.objects.filter(
                first_name__icontains=f_n,
                last_name__icontains=l_n
            )
        else:
            data = UserProfile.objects.filter(first_name__icontains=keyword) | UserProfile.objects.filter(last_name__icontains=keyword)
        serializer = UserSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)


class EditUserProfile(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        try:
            user = UserProfile.objects.get(id=request.user.id)
        except UserProfile.DoesNotExist:
            return response.HttpNotFound('User')
        if user.user_country != '':
            user.user_country = header.COUNTRY_LIST.get_county(user.user_country)
        return render(request, "chat/edit_profile.html", {
            'user_data': user,
            'country_list': header.COUNTRY_LIST.country_list()
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        try:
            user = UserProfile.objects.get(id=request.user.id)
        except UserProfile.DoesNotExist:
            return response.HttpNotFound('User')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        country = request.POST['country']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        education = request.POST['education']
        mobile = request.POST['mobile_number']
        about = request.POST['about_me']
        user.first_name = first_name
        user.last_name = last_name
        user.user_city = city
        if country != '':
            user.user_country = header.COUNTRY_LIST.get_iso_code(country)
        else:
            user.user_country = country
        user.user_birthday_day = birthday[8:]
        user.user_birthday_month = birthday[5:7]
        user.user_birthday_year = birthday[:4]
        user.user_gender = gender
        user.user_education = education
        user.user_mobile_number = mobile
        user.user_about_me = about
        user.save()
        if user.user_country != '':
            user.user_country = header.COUNTRY_LIST.get_county(user.user_country)
        return render(request, "chat/edit_profile.html", {
            'user_data': user,
            'country_list': header.COUNTRY_LIST.country_list(),
            'response_msg': 'Profile changes has been saved.'
        })


class ChatManager(APIView):

    def delete(self, request):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        friend_id = request.POST['delete_chat_room']
        try:
            ChatRoom.objects.get(author__id=request.user.id, friend__id=friend_id).delete()
        except ChatRoom.DoesNotExist:
            return response.HttpNotFound('Chat room')
        return JsonResponse({'success': 'Chat room has been deleted.'})

    def get(self, request):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        if 'msgs_amount' in request.GET and 'chat_room_data' in request.GET:
            msgs_am = len(Message.objects.filter(
                chat_room=ChatRoom.objects.get(
                    friend__id=request.GET['chat_room_data'],
                    author__id=request.user.id
                ))
            )
            response_data = {'amount': msgs_am}
            return JsonResponse(response_data)
        if 'chat_room_data' in request.GET:
            chat_room_msgs = Message.objects.filter(
                chat_room=ChatRoom.objects.get(
                    friend__id=request.GET['chat_room_data'],
                    author__id=request.user.id
                )
            )
            serializer = MessageSerializer(chat_room_msgs, many=True)
            return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if not request.user.is_authenticated:
            return response.HttpForbidden('You are not authenticated')
        msg = request.POST['msg']
        if msg != '':
            msg_time = str(datetime.now())[11:16] + "&nbsp;&nbsp;|&nbsp;&nbsp;" + str(datetime.now().strftime("%d %b %Y"))[:11]
            author = get_object_or_404(UserProfile, id=request.user.id)
            friend = get_object_or_404(UserProfile, id=request.POST['friend_id'])
            author_fname_lname = author.first_name[0] + author.last_name[0]
            try:
                chat_room = ChatRoom.objects.get(author__id=author.id, friend__id=friend.id)
            except ChatRoom.DoesNotExist:
                room_data = {
                    'author': author,
                    'friend': friend,
                    'author_id': author.id,
                    'friend_id': friend.id,
                    'logo': friend.user_logo
                }
                chat_room = functions.create_chat_room(room_data)
            message_data = {
                'chat_room': chat_room,
                'message': msg,
                'message_time': msg_time,
                'author_username': author.username,
                'author_initials': author_fname_lname,
                'author_logo': author.user_logo,
                'author_id': author.id
            }
            functions.create_message(message_data)
            if author.id != friend.id:
                try:
                    chat_room = ChatRoom.objects.get(author__id=friend.id, friend__id=author.id)
                except ChatRoom.DoesNotExist:
                    room_data = {
                        'author': friend,
                        'friend': author,
                        'author_id': friend.id,
                        'friend_id': author.id,
                        'logo': author.user_logo
                    }
                    chat_room = functions.create_chat_room(room_data)
                message_data = {
                    'chat_room': chat_room,
                    'message': msg,
                    'message_time': msg_time,
                    'author_username': author.username,
                    'author_initials': author_fname_lname,
                    'author_logo': author.user_logo,
                    'author_id': author.id
                }
                functions.create_message(message_data)
            return JsonResponse({'status_message': 'Message has been sent!'})
        return JsonResponse({'status_message': 'Message is empty!'})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/user/' + str(request.user.id))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/user/' + str(request.user.id))
            return render(request, "chat/login_form.html", {'error_message': 'Your account has been disabled'})
        return render(request, "chat/login_form.html", {'error_message': 'Invalid login or password'})
    return render(request, "chat/login_form.html")


class UserFormView(View):
    form_class = UserForm
    template_name = 'chat/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/user/' + str(request.user.id))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/user/' + str(request.user.id))
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            generated_code = form.cleaned_data['code']
            if not functions.checkUsername(username):
                form.add_error('username', 'username must be 3 characters or more')
            if not functions.checkEmail(email, UserProfile.objects.all()):
                form.add_error('email', 'account with this email address already exists')
            if not functions.checkPassword(password):
                form.add_error('password', 'password must be 8 characters or more')
            if generated_code != request.session['gen_code']:
                form.add_error('code', 'incorrect received code')
            else:
                user.set_password(password)
                user.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, "chat/index.html", {'response_msg': 'Thank you for joining us :)'})
        return render(request, self.template_name, {'form': form})


def send_email(request):
    if request.user.is_authenticated:
        return redirect('index')
    if 'generated_code' in request.GET and 'user_email' in request.GET:
        usr_email = request.GET['user_email']
        if not functions.checkEmail(usr_email, UserProfile.objects.all()):
            return JsonResponse({
                'error_code': "222",
                'name': "User with this email address already exists!"
            })
        g_c = request.GET['generated_code']
        request.session['gen_code'] = g_c
        message_content = "This is data for signing in Your account:\n\n" +\
                            " Login:           " + request.GET['username'] + "\n" +\
                            " Password:    " + request.GET['password'] + "\n\n" +\
                            "Do not show this message to anyone to prevent stealing your account!\n\n\n" +\
                            "The last step you should perform is to enter this code: " + g_c + ".\n\n\n" + \
                            "Thank You for registering on our website.\n" +\
                            "Best regards, messenger support."
        support_email = "mymessengerhelp@gmail.com"
        message_subject = 'Registration in Messenger'
        message = MIMEText(message_content)
        message['Subject'] = message_subject
        message['From'] = support_email
        message['To'] = usr_email
        new_email = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        new_email.ehlo()
        new_email.starttls()
        new_email.ehlo()
        new_email.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        new_email.sendmail(support_email, [usr_email], message.as_string())
        new_email.quit()
        return JsonResponse({'name': "Code was sent successfully!"})
    return JsonResponse({
        'error_code': "222",
        'name': "Error occurred while sending email!"
    })
