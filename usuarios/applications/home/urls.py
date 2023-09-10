""" Imports """
from django.urls import path
from . import views


""" App name """
app_name = 'home_app'


""" Patterns """
urlpatterns = [
    path('panel/', views.HomePage.as_view(), name='home'),
    path('mixin/', views.TemplatePruebaMixin.as_view(), name='mixin'),
]


