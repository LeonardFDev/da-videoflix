import os
import uuid

from django.db import models
from datetime import date
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator

class Video(models.Model):
    """Represents a video of the application."""

    def customize_file_name(instance, filenname):
        name, ext = os.path.splitext(filenname)
        new_filenname = f"video/{name}_original{ext}"

        if default_storage.exists(new_filenname):
            random_string = uuid.uuid4().hex[:7]
            return f"video/{name}_{random_string}_original{ext}"
        return new_filenname
        

    title = models.CharField(max_length=80)
    description = models.TextField(max_length=500, blank=True, default="")
    thumbnail_url = models.URLField()
    video_file = models.FileField(upload_to=customize_file_name, validators=[FileExtensionValidator(allowed_extensions=["mp4", "webm", "mov"])]) #'video'
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=date.today)


    def __str__(self):
        """Return the title and the id as a string."""
        return f"{self.title} ({self.id})"