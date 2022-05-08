import requests
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.decorators import login_required

from .forms import *


def main_search(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VINForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            vin = form.cleaned_data
            print
            return HttpResponseRedirect('/vincheck/tovar/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VINForm()

    return render(request, 'vincheck/main_search.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'vincheck/signup.html'

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


@login_required()
def avtorizovan(request):
    return render(request, 'vincheck/avtorizovan.html')


@login_required()
def personalcabinet(request):
    return render(request, 'vincheck/personalcabinet.html')


def forgotform(request):
    return render(request, 'vincheck/forgotform.html')
