from django.shortcuts import render
from django.http import JsonResponse
from .models import Books, History, Recomendations
import csv
from django.shortcuts import get_object_or_404


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
    req = get_object_or_404(Recomendations, id_client = id_client)

    book_1 = Books.objects.filter(id_book = req.req_1).first()
    if book_1 == None:
        book_1_title = ''
        book_1_author = ''
    else:
        book_1_title = book_1.title
        book_1_author = book_1.author

    book_2 = Books.objects.filter(id_book = req.req_2).first()
    if book_2 == None:
        book_2_title = ''
        book_2_author = ''
    else:
        book_2_title = book_2.title
        book_2_author = book_2.author

    book_3 = Books.objects.filter(id_book = req.req_3).first()
    if book_3 == None:
        book_3_title = ''
        book_3_author = ''
    else:
        book_3_title = book_3.title
        book_3_author = book_3.author

    book_4 = Books.objects.filter(id_book = req.req_4).first()
    if book_4 == None:
        book_4_title = ''
        book_4_author = ''
    else:
        book_4_title = book_4.title
        book_4_author = book_4.author

    book_5 = Books.objects.filter(id_book = req.req_5).first()
    if book_5 == None:
        book_5_title = ''
        book_5_author = ''
    else:
        book_5_title = book_5.title
        book_5_author = book_5.author

    history = History.objects.filter(id_client = id_client).order_by('finish_read')
    hl = []
    for h in history:
        book_history = Books.objects.filter(id_book = h.id_book).first()
        if book_history == None:
            book_history_title = ''
            book_history_author = ''
        else:
            book_history_title = book_history.title
            book_history_author = book_history.author
        i = {
            'id': h.id_client, 
            'title': book_history_title, 
            'author': book_history_author,
        }
        hl.append(i)

    if req:
        data = {
            'recommendations': [
                {'id': req.req_1, 'title': book_1_title,'author': book_1_author,},
                {'id': req.req_2, 'title': book_2_title,'author': book_2_author,},
                {'id': req.req_3, 'title': book_3_title,'author': book_3_author,},
                {'id': req.req_4, 'title': book_4_title,'author': book_4_author,},
                {'id': req.req_5, 'title': book_5_title,'author': book_5_author,}, 
                ],               
            'history': hl,
        }
    else:
        data = ''

    return JsonResponse(data)

def upload_view(request):
    do = request.GET.get('do')
    if do == 'recs':
        print('Starting load RECS...')
        read_recs()
    elif do == 'cat':
        print('Starting load CAT...')
        read_cat()
    elif do == 'history':
        print('Starting load History...')
        read_history()

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
    with open(file, encoding="utf8") as File:
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

def read_history():
    file = '/home/bourne/www/knigi/app/data/circulaton.csv'
    file_local = 'app/data/circulaton.csv'
    History.objects.all().delete()
    with open(file, encoding="utf8") as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        # row_count = sum(1 for row in reader)
        # print(row_count)
        i = 0
        for row in reader:
            i+=1

            try:
                Book = History()
                Book.id_client = row[5]
                Book.id_book = row[2]
                Book.start_read = row[3]
                Book.finish_read = row[4] 
           
                Book.save()
                print(i)               
            except:
                continue

            