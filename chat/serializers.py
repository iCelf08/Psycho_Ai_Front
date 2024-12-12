from rest_framework import serializers

from .models import Chat

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)  # You can adjust max_length as needed

class ChatResponseSerializer(serializers.Serializer):
    role = serializers.CharField()
    message = serializers.CharField()  # AI's response message



class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'user_message', 'ai_response']
