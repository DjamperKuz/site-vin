import requests
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

from .forms import *


def main_search(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VINForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            vin = form.cleaned_data
            print()
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


class RecoveryPassword(CreateView):
    form_class = CreateNewPassword
    template_name = 'vincheck/recoverypassword.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('signin')


def forgotform(request):
    if request.method == 'POST':
        form = RecoveryPassForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            mail = send_mail(subject=form.cleaned_data['username'], message='Ссылка для восстановления пароля',
                             from_email='tomaslex@mail.ru',
                             recipient_list=[user_email], fail_silently=False, auth_password='C4N9A3nkmwNm7RyAxzku')
            if mail:
                return redirect('main_search')
            else:
                messages.error(request, "Ошибка отправки")
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RecoveryPassForm()
    return render(request, 'vincheck/forgotform.html', {"form": form})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = RecoveryPassForm(request.POST)
        if password_reset_form.is_valid():
            mail = password_reset_form.cleaned_data['email']
            user = User.objects.get(email=mail)  # email в форме регистрации проверен на уникальность
            subject = 'Запрошен сброс пароля'
            email_template_name = "vincheck/email_password_reset.html"
            cont = {
                "email": user.email,
                'domain': '127.0.0.1:8000',  # доменное имя сайта
                'site_name': 'Website',  # название своего сайта
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # шифруем идентификатор
                "user": user,  # чтобы обратиться в письме по логину пользователя
                'token': default_token_generator.make_token(user),  # генерируем токен
                'protocol': 'http',
            }
            msg_html = render_to_string(email_template_name, cont)
            try:
                send_mail(subject, message='Ссылка для восстановления пароля',
                          from_email='tomaslex@mail.ru', recipient_list=[user.email], fail_silently=True,
                          html_message=msg_html, auth_password='C4N9A3nkmwNm7RyAxzku')
            except BadHeaderError:
                return HttpResponse('Обнаружен недопустимый заголовок!')
            return redirect("password_reset_done")
    else:
        password_reset_form = RecoveryPassForm()
    return render(request=request, template_name="vincheck/password_reset.html",
                  context={"password_reset_form": password_reset_form})