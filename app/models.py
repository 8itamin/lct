from os import name
from django.db import models



class Recomendations(models.Model):
    """ Модель рекомендаций

    Поля:
    ИД клиента -- Номер клиента из предоставленной базы
    Рекомендация 1 -- ИД книги из предосталвенной базы
    Рекомендация 2 -- ИД книги из предосталвенной базы
    Рекомендация 3 -- ИД книги из предосталвенной базы
    Рекомендация 4 -- ИД книги из предосталвенной базы
    Рекомендация 5 -- ИД книги из предосталвенной базы
    """
    id_client = models.CharField(max_length=50)
    req_1 = models.CharField(max_length=50)
    req_2 = models.CharField(max_length=50)
    req_3 = models.CharField(max_length=50)
    req_4 = models.CharField(max_length=50)
    req_5 = models.CharField(max_length=50)
        
    def __str__(self):
        return self.id_client
    
class Books(models.Model):
    id_book = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)