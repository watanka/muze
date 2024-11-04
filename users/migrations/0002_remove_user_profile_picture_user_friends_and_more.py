# Generated by Django 5.1.2 on 2024-11-01 05:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musics', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends_with', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='saved_songs',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='musics.song'),
        ),
        migrations.AddField(
            model_name='user',
            name='shared_songs',
            field=models.ManyToManyField(blank=True, related_name='shared_by', to='musics.song'),
        ),
        migrations.AddField(
            model_name='user',
            name='today_song',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='musics.song'),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_songs',
            field=models.ManyToManyField(blank=True, related_name='liked_by', to='musics.song'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
