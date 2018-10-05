from django.conf.urls import url
from . import views

#definido nome da aplicação para não conflitar as urls de outras aplicações
app_name = 'forum'
urlpatterns = [
    url(r'^$', views.index, name='index'),    
    #Parametro nomeado, nesse caso a view é a mesma 
    url(r'^tag/(?P<tag>[\w_-]+)/$', views.index, name='index_tagged'),
    url(r'^respostas/(?P<pk>\d+)/correta$', views.reply_correct, name='reply_correct'),
    url(r'^respostas/(?P<pk>\d+)/incorreta$', views.reply_incorrect, name='reply_incorrect'),
    url(r'^(?P<slug>[\w_-]+)/$', views.thread, name='thread'),
]