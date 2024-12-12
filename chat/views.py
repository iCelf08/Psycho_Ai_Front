from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Chat
from .serializers import ChatSerializer
import requests
from django.conf import settings

class ChatViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def create_chat(self, request):
        """
        Handle the creation of a new chat, including the message from the user and AI response.
        """
        user_message = request.data.get('message')
        chat_title = request.data.get('title', 'Untitled Chat')  # Default to 'Untitled Chat' if no title is provided
        
        if not user_message:
            return Response({"error": "No message provided."}, status=400)

        # Prepare the data for the API request
        data = {
            "model": "llama3-8b-8192",  # Replace with your actual model
            "messages": [{"role": "user", "content": user_message}]
        }

        try:
            # Send the request to the Groq API
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',  # Use the correct endpoint
                json=data,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.GROQ_API_KEY}"}
            )

            if response.status_code == 200:
                ai_message = response.json().get('choices', [{}])[0].get('message', 'No response from AI')

                # Save the chat in the database
                chat = Chat.objects.create(
                    title=chat_title,
                    user_message=user_message,
                    ai_response=ai_message
                )

                # Return the chat with a status code
                return Response({
                    "message": ai_message,
                    "chat": ChatSerializer(chat).data
                })
            else:
                return Response({"error": "Error from AI provider."}, status=500)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @action(detail=False, methods=['get'])
    def list_chats(self, request):
        """
        List all the saved chats.
        """
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def retrieve_chat(self, request, pk=None):
        """
        Retrieve a specific chat by ID.
        """
        try:
            chat = Chat.objects.get(pk=pk)
            serializer = ChatSerializer(chat)
            return Response(serializer.data)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found."}, status=404)
