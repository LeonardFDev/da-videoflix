import os
from services.tasks.convert_video import convert480p, convert720p, convert1080p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    queue = django_rq.get_queue('default', autocommit=True)

    queue.enqueue(convert480p, instance.video_file.path)
    queue.enqueue(convert720p, instance.video_file.path)
    queue.enqueue(convert1080p, instance.video_file.path)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    for resolution in ["_original.mp4", "_480p.mp4", "_720p.mp4", "_1080p.mp4"]:
        if instance.video_file:
            if os.path.isfile(instance.video_file.path.replace("_original.mp4", "") + resolution):
                os.remove(instance.video_file.path.replace("_original.mp4", "") + resolution)


    