from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Todo(models.Model):
    title = models.CharField("タスク名", max_length=30)
    description = models.TextField("詳細", blank=True)
    deadline = models.DateField("締切",null = True, blank = True)
    importance = models.IntegerField("重みづけ",validators=[MinValueValidator(1), MaxValueValidator(5)],null = True)


class TodoDay(models.Model):
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE, related_name='tododay')
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    importance = models.PositiveIntegerField()

def __str__(self):
    return self.title

def save(self, *args, **kwargs):
    super(TodoDay, self).save(*args, **kwargs)

