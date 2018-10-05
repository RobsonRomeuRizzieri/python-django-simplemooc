from django.contrib import admin

from .models import Thread, Reply

class ThreadAdmin(admin.ModelAdmin):

    list_display = ['title', 'author', 'created', 'modified']
    #author__email ele faz o join para mostrar o e-mail do autor
    search_fields = ['title', 'author__email', 'body']
    prepopulated_fields = {'slug': ('title',)}

class ReplyAdmin(admin.ModelAdmin):

    list_display = ['thread', 'author', 'correct', 'created', 'modified']
    #faz o join com assunto para listar o titulo do mesmo
    #author__email faz o join para listar o email do autor
    search_fields = ['thread__title', 'author__email', 'reply']

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)