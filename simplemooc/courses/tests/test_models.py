from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from model_mommy import mommy

from simplemooc.courses.models import Course

class CourseManagerTestCase(TestCase):

    def setUp(self):
        #_quantity - determina quantos podem ser criados
        #name - vai criar todos os registros com o valor definido para o atributo
        self.courses = mommy.make(
            'courses.Course', 
            name='Python na web com django', 
            _quantity=5
        )
        self.courses = mommy.make(
            'courses.Course', 
            name='Python para devs', 
            _quantity=10
        )        
        self.client = Client()

    def tearDown(self):
        for course in self.courses:
            course.delete()

    def test_course_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)