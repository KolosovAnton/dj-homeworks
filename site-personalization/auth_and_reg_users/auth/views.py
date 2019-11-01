from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from auth.forms import LoginForm, RegisterForm


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    template_name = 'registration/logout.html'


class UserRegisterView(CreateView):
    template_name = 'registration/signup.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        valid = super(UserRegisterView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid
