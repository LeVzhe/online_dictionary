from rest_framework.routers import DefaultRouter

from user_app import views as user_app_views

auth_router = DefaultRouter()

auth_router.register(prefix="registration", viewset=user_app_views.AuthViewset, basename="registration")
