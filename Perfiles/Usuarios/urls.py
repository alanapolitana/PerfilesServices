""" from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.routers import DefaultRouter
from Usuarios import views

router = DefaultRouter()
router.register(r'roles', views.RoleViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'), 
    path('logout/', views.Logout.as_view(), name='logout'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/', views.UserView.as_view(), name='user'),
    path('user/update/', views.UpdateUserView.as_view(), name='user_update'),
    path('', include(router.urls)),
]
 """
 
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    Login,
    Logout,
    UserView,
    UpdateUserView,
    RoleViewSet,
    BMICreateAPIView,
    BMIListAPIView,BMIChartView, ExportBMICSVView

)
from Usuarios import views

router = DefaultRouter()
router.register('roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('user/update/', UpdateUserView.as_view(), name='update-user'),
    path('bmi/create/', BMICreateAPIView.as_view(), name='bmi-create'),
    path('bmi/', BMIListAPIView.as_view(), name='bmi-list'),
    path('bmi/view/<int:user_id>/', views.view_imc, name='bmi-view'),
    path('bmi/chart/', BMIChartView.as_view(), name='bmi_chart'),
    path('bmi/export/', ExportBMICSVView.as_view(), name='export_bmi_csv'),

    path('', include(router.urls)),
]
