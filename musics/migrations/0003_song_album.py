# Generated by Django 5.1.2 on 2024-11-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='album',
            field=models.CharField(default='null', max_length=200),
            preserve_default=False,
        ),
    ]
