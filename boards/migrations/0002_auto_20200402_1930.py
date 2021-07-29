# Generated by Django 2.2.11 on 2020-04-02 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='topic',
            name='subject',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
