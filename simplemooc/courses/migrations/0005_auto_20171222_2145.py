# Generated by Django 2.0 on 2017-12-22 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20171222_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollments', to='courses.Course', verbose_name='Curso'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollments', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
