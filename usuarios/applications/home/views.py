""" Imports """
import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy


""" Mixin """
class FechaMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha"] = datetime.datetime.now()
        return context


""" Home page """
class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'
    login_url = reverse_lazy('users_app:login')
    

""" Mixin Test """
class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = 'home/mixin.html'
    
    
    
    

