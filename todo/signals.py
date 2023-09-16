from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Color



COLORS = ['orangered','orange','khaki','palegreen','limegreen','mediumspringgreen','deepskyblue','royalblue','darkviolet','plum','pink','deeppink']

@receiver(post_save, sender=User)
def create_default_colors(sender, instance, created, **kwargs):
    if created:
        # Create colors
        for color in COLORS:
            Color.objects.create(user=instance, name=color)
