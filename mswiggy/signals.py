from .models import UpdateLocation
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=UpdateLocation)
def index_location(sender, instance, **kwargs):
	instance.indexing()

