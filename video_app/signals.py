import shutil
import django_rq

from pathlib import Path
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Video
from services.tasks.convert_video import convert_and_create_hls

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(convert_and_create_hls, instance.video_file.path, instance.id)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        path = Path(instance.video_file.path).parent

        if path.is_dir():
            shutil.rmtree(path)