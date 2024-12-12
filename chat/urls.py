from rest_framework.routers import DefaultRouter
from .views import ChatViewSet

router = DefaultRouter()
router.register(r'chat', ChatViewSet, basename='chat')

urlpatterns = [
    # Other URLs
] + router.urls
