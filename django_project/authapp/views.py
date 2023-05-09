from django.contrib import auth, messages
from django.shortcuts import render
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, ShopUserProfileEditForm
from django.urls import reverse_lazy
from basket.models import Basket
from authapp.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from .utils import send_verify_mail
from django.shortcuts import get_object_or_404



class LoginCreateView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'authapp/login.html'

    def dispatch(self, request, *args, **kwargs):
        return super(LoginCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = reverse_lazy('index')
        return url


class ProfileCreateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'authapp/profile.html'
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_profile'] = ShopUserProfileEditForm(instance=self.request.user.shopuserprofile)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


class RegisterCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterCreateView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            send_verify_mail(user)
            messages.success(request, message='Проверьте почту')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        return super(LogoutUserView, self).dispatch(request, *args, **kwargs)


def verify(request, user_id, hash):
    user = get_object_or_404(User, pk=user_id)
    if user.activation_key == hash and not user.is_activation_key_expires():
        user.is_active = True
        user.activation_key = None
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return render(request, 'authapp/verification.html')
