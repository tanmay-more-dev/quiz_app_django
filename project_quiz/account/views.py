from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    next_page = reverse_lazy('dashboard:home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('public:home')
