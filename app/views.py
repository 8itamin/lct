from django.shortcuts import render
from django.http import JsonResponse


def Home(request):
    """
    Template - Index page
    """
    return render(request, 'app/index.html', context = {'username': request.user, })

def my_api_view(request):
    """
    Request page:
    in - Json ID 
    out - Json
            recommendations (id, title, author),
            history (id, title, author) 
    """
    data = {
        'recommendations': {
            'id': '789',
            'title': 'Красная шапочка',
            'author': 'Пьерро',
            },
        'history': {
            'id': '123',
            'title': 'Незнайка на луне',
            'author': 'Носов',
            }
    }
    return JsonResponse(data)