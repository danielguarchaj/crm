from django.urls import path, include
from rest_framework import routers


from . import views

app_name = 'crm_client'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]