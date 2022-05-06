from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


def main_search(request):
    return render(request, 'vincheck/main_search.html')


class Signin(CreateView):
    form_class = RegisterUserForm
    template_name = 'vincheck/signin.html'
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('signin')


def tovar(request):
    return render(request, 'vincheck/tovar.html')


def avtorizovan(request):
    return render(request, 'vincheck/avtorizovan.html')


def forgotform(request):
    return render(request, 'vincheck/forgotform.html')
