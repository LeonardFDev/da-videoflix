from django.db import models
from django.core.validators import FileExtensionValidator

class Video(models.Model):
    """Represents a video of the application."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    thumbnail_url = models.URLField()
    video_file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["mp4", "webm", "mov"])])
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the title and the id as a string."""
        return f"{self.title} ({self.id})"