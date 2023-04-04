from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.urls import reverse_lazy
from basket.models import Basket
from authapp.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator


class LoginCreateView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'authapp/login.html'

    def dispatch(self, request, *args, **kwargs):
        return super(LoginCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = reverse_lazy('index')
        return url


class ProfileCreateView(CreateView):
    model = User
    form_class = UserProfileForm
    template_name = 'authapp/profile.html'
    success_url = 'auth:profile'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


class RegisterCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterCreateView, self).dispatch(request, *args, **kwargs)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        return super(LogoutUserView, self).dispatch(request, *args, **kwargs)
