from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.Home, name='home'), 
    path('knigi-api/', views.my_api_view),
    path('upload/', views.upload_view),

    
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)