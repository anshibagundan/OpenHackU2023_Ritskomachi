# Generated by Django 4.2.4 on 2023-09-15 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('orangered', 'red'), ('orange', 'orange'), ('khaki', 'yellow'), ('palegreen', 'lightgreen'), ('limegreen', 'green'), ('mediumspringgreen', 'emegreen'), ('deepskyblue', 'lightblue'), ('royalblue', 'blue'), ('darkviolet', 'purple'), ('plum', 'purplepink'), ('pink', 'pink'), ('deeppink', 'deeppink')], max_length=17)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('color_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todo.color')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'color_id')},
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='タスク名')),
                ('description', models.TextField(blank=True, verbose_name='詳細')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='締切')),
                ('importance', models.PositiveIntegerField(choices=[(1, 'とても大事'), (2, '大事'), (3, '普通'), (4, 'あまり大事じゃない'), (5, '全然大事じゃない')], default=3)),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todo.tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TodoDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('deadline', models.DateField()),
                ('importance', models.PositiveIntegerField()),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todo.tag')),
                ('todo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tododay', to='todo.todo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
