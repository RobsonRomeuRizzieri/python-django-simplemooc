from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread

#Apartir de TemplateView
#class ForumView(TemplateView):
    
#    template_name = 'forum/index.html'    

#apartir de View
#class ForumView(View):
        
#    def get(self, request, *args, **kwargs):
#        return render(request, 'forum/index.html')

#apartir de ListView
class ForumView(ListView):

    model = Thread
    paginate_by = 2
    template_name = 'forum/index.html'
 
    def get_context_data(self, **kwargs):
        #Chama a base do método
        context = super(ForumView, self).get_context_data(**kwargs)
        #Relaciona todas as tags ao tópico
        context['tags'] = Thread.tags.all() 
        return context

index = ForumView.as_view()

#poderia também ter feito dessa forma em vez de criar a class
#index = TemplateView.as_wiew(template_name='forum/index.html')