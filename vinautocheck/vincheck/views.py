import json

from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.cache import cache

from .parsers.main_pars import pars_without_reestor_rb

from .forms import *


# главная страница
def main_search(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VINForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            vin = form.cleaned_data
            cache.set('user_vin', vin['vin'])
            print(vin)
            return HttpResponseRedirect('tovar')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VINForm()

    return render(request=request, template_name='vincheck/main_search.html', context={'form': form})


# регистрация пользователя
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'vincheck/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main_search')


# вход в аккаунт
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'vincheck/signin.html'

    def get_success_url(self):
        return reverse_lazy('main_search')


# выход из аккаунта
def logout_user(request):
    logout(request)
    return redirect('signin')


# страница с выбором товара
@login_required()
def tovar(request):
    return render(request, 'vincheck/tovar.html')


@login_required()
def personalcabinet(request):
    return render(request, 'vincheck/personalcabinet.html')


# страница с чекбоксом
@login_required()
def check_box(request):
    vin = cache.get('user_vin')
    data = {"message": vin}
    return render(request, 'vincheck/check_box.html', context=data)


@login_required()
def online_document(request):
    vin = cache.get('user_vin')
    data_json = {
    "history": {
        "data": {
            "requestTime": "15.05.2022 18:29",
            "RequestResult": {
                "ownershipPeriods": {
                    "ownershipPeriod": [
                        {
                            "lastOperation": "69",
                            "simplePersonType": "Natural",
                            "from": "2009-11-12",
                            "to": "2009-11-12"
                        },
                        {
                            "lastOperation": "62",
                            "simplePersonType": "Natural",
                            "from": "2009-11-12",
                            "to": "2009-11-30"
                        },
                        {
                            "lastOperation": "62",
                            "simplePersonType": "Natural",
                            "from": "2009-12-10",
                            "to": "2010-03-23"
                        },
                        {
                            "lastOperation": "62",
                            "simplePersonType": "Natural",
                            "from": "2010-03-30",
                            "to": "2011-09-07"
                        },
                        {
                            "lastOperation": "12",
                            "simplePersonType": "Natural",
                            "from": "2011-09-26",
                            "to": "2016-08-30"
                        },
                        {
                            "lastOperation": "07",
                            "simplePersonType": "Natural",
                            "from": "2016-08-30",
                            "to": "2022-02-10"
                        },
                        {
                            "lastOperation": "02",
                            "simplePersonType": "Natural",
                            "from": "2022-03-05"
                        }
                    ]
                },
                "vehiclePassport": {},
                "vehicle": {
                    "engineVolume": "1596.0",
                    "color": "ГРАФИТОВЫЙ МЕТАЛ.",
                    "bodyNumber": "XTA21144094786239",
                    "year": "2009",
                    "engineNumber": "5126356",
                    "vin": "XTA21144094786239",
                    "model": "ВАЗ 211440 LADA SAMARA ",
                    "category": "В",
                    "type": "22",
                    "powerHp": "81.0",
                    "powerKwt": "60"
                }
            },
            "hostname": "h6-check2-dc",
            "vin": "XTA21144094786239",
            "regnum": "",
            "message": "ver.3.3",
            "registerToken": "17411612e1461d81941f21c117a1a71c11d619e1931df11a",
            "status": 200
        },
        "success": 'true'
    },
    "dtp": {
        "data": {
            "requestTime": "15.05.2022 18:29",
            "RequestResult": {
                "errorDescription": "",
                "statusCode": 1,
                "Accidents": []
            },
            "hostname": "h6-check2-dc",
            "vin": "XTA21144094786239",
            "status": 200
        },
        "success": 'true'
    },
    "wanted": {
        "data": {
            "requestTime": "15.05.2022 18:29",
            "RequestResult": {
                "records": [],
                "count": 0,
                "error": 0
            },
            "hostname": "h1-dc",
            "vin": "XTA21144094786239",
            "status": 200
        },
        "success": 'true'
    },
    "restrict": {
        "data": {
            "requestTime": "15.05.2022 18:30",
            "RequestResult": {
                "records": [],
                "count": 0,
                "error": 0
            },
            "hostname": "h6-check2-dc",
            "vin": "XTA21144094786239",
            "status": 200
        },
        "success": 'true'
    },
    "diagnostic": {
        "data": {
            "requestTime": "15.05.2022 18:30",
            "RequestResult": {
                "diagnosticCards": [
                    {
                        "dcExpirationDate": "2023-03-04",
                        "pointAddress": "363331, Северная Осетия - Алания Республика, Ардон г., Ардонский р-н., Алагирская ул., дом 18, ",
                        "chassis": "",
                        "body": "",
                        "operatorName": "11878",
                        "pdfBase64": 'null',
                        "odometerValue": "179919",
                        "dcNumber": "118781012200443",
                        "dcDate": "2022-03-04",
                        "previousDcs": [
                            {
                                "odometerValue": "201532",
                                "dcExpirationDate": "2022-01-16",
                                "dcNumber": "106320012100382",
                                "dcDate": "2021-01-15"
                            }
                        ],
                        "success": 'true',
                        "vin": "XTA21144094786239",
                        "model": "211440",
                        "brand": "LADA (ВАЗ)"
                    }
                ],
                "error": 'null',
                "status": "OK"
            },
            "hostname": "h6-check1-dc",
            "vin": "XTA21144094786239",
            "status": 200
        },
        "success": 'true'
    }
}
    # data_json = pars_without_reestor_rb(vin)
    return render(request, 'vincheck/onlinedocument.html', context=data_json)


# страница с чекбоксом 2
@login_required()
def check_box2(request):
    vin = cache.get('user_vin')
    data = {"message": vin, "checkbox": 10}
    if request.method == "POST":
        checkbox = request.POST.getlist('checkbox_1')

        if checkbox == ['checkbox_1']:
            data['checkbox'] = 20
        else:
            data['checkbox'] = 10
        return render(request, "vincheck/check_box2.html", context=data)

    return render(request, 'vincheck/check_box2.html', context=data)


@login_required()
def form_pay(request):
    return render(request, 'vincheck/formofpayment.html')


# восстановление пароля с помощью почты
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


def index(request):
    return render(request, 'vincheck/index.html')


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'vincheck/password_reset_confirm.html'

