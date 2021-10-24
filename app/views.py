from django.shortcuts import render
from django.http import JsonResponse
from .models import Books, Recomendations
import csv


def Home(request):
    """
    Template - Index page
    """
    if request.method == 'POST':
        id_client = request.POST.get('id_client')
        req = Recomendations.objects.filter(id_client = id_client).first
        
        return render(request, 'app/index.html', context = {'username': request.user, })
    else:          
        
        return render(request, 'app/index.html', context = {'username': request.user, })

def my_api_view(request):
    """
    Request page:
    in - GET ID 
    out - Json
            recommendations 5 (id, title, author),
            history 5 (id, title, author) 
    """

    id_client = request.GET.get('id_client')
    req = Recomendations.objects.filter(id_client = id_client).first


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

def upload_view(request):
    do = request.GET.get('do')
    if do == 'recs':
        print('Starting load RECS...')
        read_recs()
    elif do == 'cat':
        print('Starting load CAT...')
        read_cat()

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


def read_recs():
    file = '/home/bourne/www/knigi/app/data/recs.csv'
    file_local = 'app/data/recs.csv'
    Recomendations.objects.all().delete()
    i=0
    with open(file) as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)        
        for row in reader:        
            i+=1    
            Rec = Recomendations()
            try:
                Rec.id_client = row[0]
                Rec.req_1 = row[1][:row[1].find('.')]
                Rec.req_2 = row[2][:row[2].find('.')]
                Rec.req_3 = row[3][:row[3].find('.')]
                Rec.req_4 = row[4][:row[4].find('.')]
                Rec.req_5 = row[5][:row[5].find('.')]
                Rec.save()               
            except:
                continue 
            print(i)

def read_cat():
    file = '/home/bourne/www/knigi/app/data/cat.csv'
    file_local = 'app/data/cat.csv'
    Books.objects.all().delete()
    with open(file_local, encoding="utf8") as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        i = 0
        for row in reader:
            i+=1

            try:
                title = str(row[7])
                clear_title = title.replace('"', "")
                id = str(row[1])
                author = str(row[6])

                Book = Books()
                Book.id_book = id
                Book.title = clear_title
                Book.author = author  
           
                Book.save()
                print(i)               
            except:
                continue

            