"""Video post save and Video post delete sginals"""

import shutil
import django_rq

from pathlib import Path
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Video
from services.tasks.convert_video import convert_and_create_hls

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """After the video object is created, a Taks is created that converts the videos"""
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(convert_and_create_hls, instance.video_file.path, instance.id)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """After deleting the video object, 
    checks if the video path exists and deletes the folder where the video path is located"""

    if instance.video_file:
        path = Path(instance.video_file.path).parent

        if path.is_dir():
            shutil.rmtree(path)