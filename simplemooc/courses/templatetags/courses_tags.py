from django.template import Library
from simplemooc.courses.models import Enrollment

register = Library()


@register.inclusion_tag('courses/templatetags/my_courses.html')
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user)
    context = {
        'enrollments' : enrollments
    }
    return context

#Esse register permite atualizar os valores no contexto
#@register.assignment_tag usado em versões menores que a 2
@register.simple_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)
