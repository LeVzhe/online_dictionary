from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from user_app import urls as user_app_routers

router = routers.DefaultRouter()

API_V1_URL_PATH = "api/"

registries = [
    user_app_routers.auth_router.registry,
]

for registry in registries:
    router.registry.extend(registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_V1_URL_PATH, include(router.urls)),
    path(
        "docs/download/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]
