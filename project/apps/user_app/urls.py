from rest_framework.routers import DefaultRouter

from apps.user_app import views as user_app_views

auth_router = DefaultRouter()
user_router = DefaultRouter()

auth_router.register(
    prefix="registration",
    viewset=user_app_views.AuthViewset,
    basename="registration",
)
user_router.register(
    prefix="user",
    viewset=user_app_views.UserViewset,
    basename="user",
)
