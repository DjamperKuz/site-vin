from django.shortcuts import render


def main_search(request):
    return render(request, 'vincheck/main_search.html')


def signin(request):
    return render(request, 'vincheck/signin.html')


def tovar(request):
    return render(request, 'vincheck/tovar.html')


def avtorizovan(request):
    return render(request, 'vincheck/avtorizovan.html')


def forgotform(request):
    return render(request, 'vincheck/forgotform.html')
