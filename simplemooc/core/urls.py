from django.conf.urls import url
from . import views

#definido nome da aplicação para não conflitar as urls de outras aplicações
app_name = 'core'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^contato/$', views.contact, name='contato'),
]