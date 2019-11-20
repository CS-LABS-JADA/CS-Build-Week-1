from rest_framework import routers

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include

from rest_framework.authtoken import views

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/adv/', include('adventure.urls')),
    path('api/login/', views.obtain_auth_token),
    path('api/register/', include('rest_auth.urls')),
]
