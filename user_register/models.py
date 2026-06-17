from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="Номер телефона в формате E.164, например +996555123456",
    )
    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        help_text="Telegram user ID",
    )

    def __str__(self):
        return f"Profile({self.user.username})"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)
