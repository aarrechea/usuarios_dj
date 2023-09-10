""" Imports """
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm
from .models import User
from .functions import code_generator


""" User register form view """
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        codigo = code_generator
        
        user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombre = form.cleaned_data['nombre'],
            apellido = form.cleaned_data['apellido'],
            gender = form.cleaned_data['gender'],
            cod_registro = codigo
        )
        
        # Sending email confirmation
        ASUNTO = 'Confirmación de email'
        MENSAJE = f'Código de verificación {codigo}'
        EMAIL_REMITENTE = 'email@email.com'
        send_mail(ASUNTO, MENSAJE, EMAIL_REMITENTE, [form.cleaned_data['email'],])
                
        return HttpResponseRedirect(
            reverse(
                'users_app:verification',
                kwargs={'pk':user.id}
            )
        )


""" Login Class """
class Login(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home')
    
    def form_valid(self, form):
        print(f"Username: {form.cleaned_data['username']} - Password: {form.cleaned_data['password']}")
        
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        
        login(self.request, user)
        
        return super(Login, self).form_valid(form)


""" Logout Class """
class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        
        return HttpResponseRedirect(reverse('users_app:login'))


""" Update Password """
class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    
    def form_valid(self, form):
        user = self.request.user
        
        user = authenticate(
            username=user.username,
            password=form.cleaned_data['password1'],
        )
        if user:
            new_password = self.cleaned_data['password2']
            user.set_password(new_password)
            user.save()
            
        logout(self.request)            
                    
        return super().form_valid(form)


""" Verification email code """
class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:login')
    
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk']
        })
        
        return kwargs
    
    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(is_active=True)
        
        return super().form_valid(form)



