from django.db import models
from django.conf import settings
from django.utils import timezone

from simplemooc.core.mail import send_mail_template

class CourseManager(models.Manager):

    #esse método vai permitir pesquisar no nome e na descrição ao mesmo tempo
    def search(self, query):
        #Dessa forma permite fazer o filtro nos campos com OU
        return self.get_queryset().filter(
            # | esse é o OU
            # \ permite fazer a quebra de linha sem o python achar que já acabou o comando
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )
        #Dessa forma filtra usando o and, e precisaria ter o valor nos dois campos
        #return self.get_queryset().filter(
        #    name__incontains=query, description__icontains=query
        #)

# Create your models here.
class Course(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descrição', blank=True)
    about = models.TextField('Sobre o curso', blank=True)
    #blank = campo não é obrigatório
    start_date = models.DateField(
        'Data de Inínico', null=True, blank=True
    )
    #Vai colocar as imagens dentro da pasta settings.py MEDIA_ROOT = os.path.join(BASE_DIR, 'simplemooc', 'media')
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
    )
    #auto_now_add = sempre que for adicionado
    created_at = models.DateTimeField(
        'Criado em', auto_now_add=True
    )
    #auto_now = sempre que for salvo
    updated_at = models.DateTimeField(
        'Atualizado em', auto_now=True
    )
    #Agora não é mais o course manager padrão mas sim o que customizamos
    #Continuamos a ter os outros recursos como filter, all ...
    #Agora também temos o search que verifica o valor nos dois atributos
    objects = CourseManager()

    #por padrão é retornado sempre o object para isso vamos modificar o create
    #para listar o nome e não o object
    def __str__(self):
        return self.name

    #retornar uma tupla da url e argumentos não nomeaveis, depois argumentos nomeaveis    
    #Metodo para simplificar a definição da url
    @models.permalink
    def get_absolute_url(self):
        #(pagina do model, argumentos não nomeavais, argumentos nomeaveis)
        return ('courses:details', (), {'slug' :self.slug})

    def release_lessons(self):
        today = timezone.now().date()
        #retorna todas as aulas disponiveis apartir da data atual 
        return self.lessons.filter(release_date__lte=today)

    #Permite definir verboso name para apresentar um nome melhor para a classe     
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        #Permite definir uma lista de campos para fazer a ordenação
        #-name altera para decrescente
        ordering = ['-name']


class Lesson(models.Model):
    
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número (Ordem)', blank=True, default=0)
    release_date = models.DateField('Data de liberação', blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='Curso', related_name='lessons')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name

    def is_available(self):
        if self.release_date:            
            today = timezone.now().date()
            return self.release_date >= today
        return False

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']

class Material(models.Model):
    
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True)
    file = models.FileField(upload_to='lessons/materials', blank=True, null=True)

    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='Aula', related_name='materials')

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Matérial'
        verbose_name_plural = 'Materiais'



#Inscrição
class Enrollment(models.Model):

    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        verbose_name='Usuário', related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, 
        verbose_name='Curso', related_name='enrollments'
    )
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=1, blank=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        #Determina que uma inscrição só pode ter um usuário e um curso relacionados
        unique_together = (('user', 'course'),)

class Announcement(models.Model):

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, verbose_name='Curso', related_name='announcement')
    title = models.CharField('Título', max_length=100)
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']

class Comment(models.Model):

    announcement = models.ForeignKey(
        Announcement, on_delete=models.PROTECT, verbose_name='Anúnico', related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='usuário'
    )
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

def post_save_announcement(sender, instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement' : instance
        }
        template_name = 'courses/announcement_email.html'
        enrollments = Enrollment.objects.filter(
            course=instance.course, status=1
        )
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]        
            send_mail_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(
    post_save_announcement, 
    sender=Announcement,
    dispatch_uid='post_save_announcement'
)


