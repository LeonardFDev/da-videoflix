import os
import uuid

from django.db import models
from datetime import date
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator

class Video(models.Model):
    """Represents a video of the application."""

    title = models.CharField(max_length=80)
    description = models.TextField(max_length=500, blank=True, default="")
    thumbnail_url = models.ImageField(upload_to="video", default="")
    video_file = models.FileField(upload_to="video", validators=[FileExtensionValidator(allowed_extensions=["mp4", "webm", "mov"])])
    category = models.CharField(max_length=100, default="Private")
    created_at = models.DateTimeField(default=date.today)


    def __str__(self):
        """Return the title and the id as a string."""
        return f"{self.title} ({self.id})"