from django.db import models

# Create your models here.
from django.db import models

class Chat(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user_message = models.TextField()
    ai_response = models.TextField()

    def __str__(self):
        return self.title
