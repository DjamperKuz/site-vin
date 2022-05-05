from django.urls import path

from .views import *


urlpatterns = [
    path('', main_search, name='main_search'),
    path('signin/', signin, name='signin'),
    path('tovar/', tovar, name='tovar'),
    path('avtorizovan/', avtorizovan, name='avtorizovan'),
    path('forgotform/', forgotform, name='forgotform')
]
