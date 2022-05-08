import requests
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import *


def main_search(request):
    return render(request, 'vincheck/main_search.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'vincheck/signup.html'
    # success_url = reverse_lazy('signin')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('avtorizovan')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'vincheck/signin.html'

    def get_success_url(self):
        return reverse_lazy('avtorizovan')


def logout_user(request):
    logout(request)
    return redirect('signin')


def tovar(request):
    return render(request, 'vincheck/tovar.html')


def avtorizovan(request):
    return render(request, 'vincheck/avtorizovan.html')


def personalcabinet(request):
    return render(request, 'vincheck/personalcabinet.html')


def forgotform(request):
    return render(request, 'vincheck/forgotform.html')
