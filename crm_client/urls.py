from django.urls import path, include
from rest_framework import routers


from . import views

app_name = 'crm_client'

router = routers.DefaultRouter()
router.register('clientes', views.ClienteViewSet, basename='clientes')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('dashboard/', views.DashboardAPIView.as_view(), name='dashboard'),
    path('departamentos/', views.DepartamentoListAPIView.as_view(), name='departamentos'),
    path('clientes_search/', views.ClientSearchAPIView.as_view(), name='clientes_search'),
]