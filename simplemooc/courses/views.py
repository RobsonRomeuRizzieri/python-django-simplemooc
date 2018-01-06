from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required

# Create your views here.
def index(request):
    courses = Course.objects.all()
    template_name = 'courses/index.html'
    context = {
        'courses': courses
    }
    return render(request, template_name, context)

#método para obter os valores com ID
#def details(request, pk):
    #course = Course.objects.get(pk=pk)
    #vai retornar pagina não encontrada caso receber um código que não existe
#    course = get_object_or_404(Course, pk=pk)
#    template_name = 'courses/details.html'
#    context = {
#        'course': course
#    }    
#    return render(request, template_name, context)

def details(request, slug):
    #vai retornar pagina não encontrada caso receber um código que não existe
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            #criado método no form para enviar o e-mail
            form.send_mail(course)
            #Lista todos os campos do formulário
            print(form.cleaned_data)
            #Permite acessar somente um campo especifico do formulário
            print(form.cleaned_data['name'])
            #limpa formulário porque recebe a classe sem nada
            form = ContactCourse()
            
    else:
        form = ContactCourse()
        
    template_name = 'courses/details.html'
    context['course'] = course
    context['form'] = form    
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user = request.user, course = course
    )
    #Foi alterado para criar ativo por padrão
    if created:
    #    enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')
    return redirect('accounts:dashboard')

@login_required
@enrollment_required
def announcements(request, slug):
    #O curso foi adicionado ao request dentro do decorator @enrollment_required 
    #por esse motivo pode acessar o curso usando request.course
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course' : course,
        'announcements' : course.announcement.all()
    }
    return render(request, template, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    #O curso foi adicionado ao request dentro do decorator @enrollment_required 
    #por esse motivo pode acessar o curso usando request.course
    course = request.course
    #Não precisa mais repetir o código abaixo pode que o mesmo está no decorator @enrollment_required 
    #course = get_object_or_404(Course, slug=slug)
    #if request.user.is_staff:
    #    enrollment = get_object_or_404(
    #        Enrollment, user=request.user, course=course
    #    )
    #    if not enrollment.is_approved():
    #        messages.error(request, 'A sua inscrição está pendente')
    #        return redirect('accounts:dashboard')
    announcement = get_object_or_404(course.announcement.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso')
    template = 'courses/show_announcement.html'
    announcement = get_object_or_404(course.announcement.all(), pk=pk)
    context = {
        'course' : course,
        'announcement' : announcement,
        'form' : form,
    }
    return render(request, template, context)

@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template = 'courses/lessons.html'
    lessons = course.release_lessons()
    #Se for o usuário adiministrador lista todas as aulas
    if request.user.is_staff:
        lessons = course.lessons.all()
    context = {
        'course' : course
    }
    return render(request, template, context)

@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Está aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)
    template = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request, template, context)

@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        return redirect(material.file.url)
    template = 'courses/material.html'
    print('robson')
    print(course)
    context = {
        'course' : course,
        'lesson' : lesson,
        'material' : material
    }
    return render(request, template, context)

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
       'enrollment' : enrollment,
       'course': course,
    }
    return render(request, template, context)