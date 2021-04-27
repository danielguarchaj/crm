from django.urls import path, include
from rest_framework import routers


from . import views

app_name = 'crm_client'

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]