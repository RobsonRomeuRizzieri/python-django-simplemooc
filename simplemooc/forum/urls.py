from django.conf.urls import url
from . import views

#definido nome da aplicação para não conflitar as urls de outras aplicações
app_name = 'forum'
urlpatterns = [
    url(r'^$', views.index, name='index'),    
]