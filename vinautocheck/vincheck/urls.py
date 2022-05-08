from django.urls import path

from .views import *


urlpatterns = [
    path('', main_search, name='main_search'),
    path('signup/', RegisterUser.as_view(), name='signup'),
    path('signin/', LoginUser.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('tovar/', tovar, name='tovar'),
    path('avtorizovan/', avtorizovan, name='avtorizovan'),
    path('personalcabinet/', personalcabinet, name='personalcabinet'),
    path('forgotform/', forgotform, name='forgotform'),
    path('recoverypassword/', RecoveryPassword.as_view(), name='recoverypassword')
]
