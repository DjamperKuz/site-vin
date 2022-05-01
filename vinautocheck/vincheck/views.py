from django.shortcuts import render


def main_search(request):
    return render(request, 'vincheck/main_search.html')
