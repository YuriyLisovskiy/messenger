from rest_framework import serializers
from .models import Message, UserProfile, ChatRoom


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('user_logo', 'first_name', 'last_name', 'id')

class ChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRoom
        fields = '__all__'
