from django.contrib import admin
   
from .models import Course, Enrollment, Announcement, Comment, Material, Lesson
# Register your models here.

#Classe de configurações do admins
class CourseAdmin(admin.ModelAdmin):

    #Permite definir quais campos devem aparecer na tela de consulta do admin
    list_display = ['name', 'slug', 'start_date', 'created_at']
    #Lista de campos para permitir a pesquisa
    search_fields = ['name', 'slug']
    #Determina uma lista de campos para pré-definir valor para outro campo
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Course, CourseAdmin) 
admin.site.register([Enrollment, Announcement, Comment, Material]) 

#Pode ser listado os campos na vertial usando a deinição abaixo
#class MaterialInlineAdmin(admin.TabularInline):
class MaterialInlineAdmin(admin.StackedInline):

    model = Material


class LessonAdmin(admin.ModelAdmin):

    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    inlines = [
        MaterialInlineAdmin
    ]

admin.site.register(Lesson, LessonAdmin)