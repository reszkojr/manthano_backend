from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import ManthanoUser, Profile


@receiver(post_save, sender=ManthanoUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
