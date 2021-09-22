from django.db import models
from imagekit import processors
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Post(models.Model):
    id_name = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='images/')
    image = ProcessedImageField(upload_to='images/',
                                processors=[ResizeToFill(300,300)],
                                format='JPEG',
                                options={'quality': 100})
    def __str__(self):
        return self.content