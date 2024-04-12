from django.shortcuts import render, HttpResponse


def index_controller(request, menu_path: str = None):
    context = {'menu_path': menu_path}
    return render(request, 'index.html', context=context)
