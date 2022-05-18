from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', main_search, name='main_search'),
    path('signup/', RegisterUser.as_view(), name='signup'),
    path('signin/', LoginUser.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('tovar/', tovar, name='tovar'),
    path('personalcabinet/', personalcabinet, name='personalcabinet'),
    # path('recoverypassword/', RecoveryPassword.as_view(), name='recoverypassword'),
    path('tovar/checkbox/', check_box, name='checkbox'),
    path('tovar/checkbox/onlinedocument', online_document, name='online_document'),
    path('tovar/checkbox2/', check_box2, name='checkbox2'),
    path('form_of_payment/', form_pay, name='form_of_payment'),
    path('personalcabinet/my_inf/', my_inf, name='my_inf'),

    # смена пароля с помощью почты
    path("password-reset/", password_reset_request, name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='vincheck/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name='vincheck/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='vincheck/password_reset_complete.html'), name="password_reset_complete"),
    # path('change-password/', auth_views.change_password, {'post_change_redirect': 'next_page'}, name='password_change'),
]
