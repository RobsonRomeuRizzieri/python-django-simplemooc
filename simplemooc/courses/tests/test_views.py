from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from simplemooc.courses.models import Course

class ContactCourseTestcase(TestCase):
    
    #Permite definir valor no banco de dados
    def setUp(self):
        self.course = Course.objects.create(name='Django', slug='django')

    #Remover os valores do banco
    def tearDown(self):
        self.course.delete()

    #Permitir inicializar os valores da classe
    #@classmethod
    #def setUpClass(cls):
    #    pass
    #Permitir inicializar os valores da classe
    #@classmethod
    #def tearDownClass(cls):
    #    pass

    #def test_courses_details_status_code(self):
    #    client = Client()
    #    response = client.get(reverse('courses:details'))
    #    self.assertEqual(response.status_code, 200)

    def test_contact_form_error(self):
        data = {'name': 'Fulano de tal', 'email': '', 'message': ''}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_contact_form_success(self):
        data = {'name': 'Fulano de tal', 'email': 'admin@admin.com', 'message': 'Oi'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])