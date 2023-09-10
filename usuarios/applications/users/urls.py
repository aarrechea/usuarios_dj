""" Imports """
from django.urls import path
from . import views


""" Name """
app_name = 'users_app'

""" Patterns """
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('update/', views.UpdatePassword.as_view(), name='update'),
    path('verification/<pk>/', views.CodeVerificationView.as_view(), name='verification'),
]


