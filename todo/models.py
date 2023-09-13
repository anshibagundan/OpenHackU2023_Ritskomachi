from django.db import models

from django.contrib.auth.models import User

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("タスク名", max_length=30)
    description = models.TextField("詳細", blank=True)
    deadline = models.DateField("締切",null = True, blank = True)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE, default='')

    VERY_IMPORTANT = 1
    IMPORTANT = 2
    NORMAL = 3
    NOT_SO_IMPORTANT = 4
    NOT_IMPORTANT = 5

    IMPORTANCE_CHOICES = [
        (VERY_IMPORTANT, 'とても大事'),
        (IMPORTANT, '大事'),
        (NORMAL, '普通'),
        (NOT_SO_IMPORTANT, 'あまり大事じゃない'),
        (NOT_IMPORTANT, '全然大事じゃない'),
    ]

    importance = models.PositiveIntegerField(choices=IMPORTANCE_CHOICES, default=NORMAL)



class TodoDay(models.Model):
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE, related_name='tododay')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    importance = models.PositiveIntegerField()
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(TodoDay, self).save(*args, **kwargs)

