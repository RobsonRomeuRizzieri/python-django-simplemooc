"""simplemooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
#from simplemooc.core import 
#from . import views

admin.autodiscover()

urlpatterns = [

    path('admin/', admin.site.urls),
    #permite adicionar outros arquivos de urls usado quando queremos que cada aplicação tenha seu aquivo de urls 
    #path('community/', include('aggregator.urls')),

    #vai pegar as rotas/urls da aplicação core
    #url(r'', include('simplemooc.core.urls')), assim ou como esta abaixo   
    #path('', include('simplemooc.core.urls')),    
    #Adicionado namespace para evitar dar erro para aplicacoes com a mesma url
    path('', include('simplemooc.core.urls')),
    path('conta/', include('simplemooc.accounts.urls')),
    path('cursos/', include('simplemooc.courses.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)