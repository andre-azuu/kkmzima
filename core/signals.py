# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Farmer, Consumer

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_farmer:
        Farmer.objects.create(user=instance, farmerUsername=instance.username)
    elif created and instance.is_consumer:
        Consumer.objects.create(user=instance, consumerUsername=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_farmer:
        instance.Farmer.save()
    elif instance.is_consumer:
        instance.Consumer.save()
