# In destinations/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import os
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def destination_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/destinations/<destination_id>/<filename>
    ext = filename.split('.')[-1]
    filename = f"{instance.id}_{instance.destination.id}.{ext}"
    return os.path.join('destinations', str(instance.destination.id), filename)

class Destination(models.Model):
    place_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    weather = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    google_map_link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.place_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.place_name)
        super().save(*args, **kwargs)

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=destination_image_path)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.destination.place_name}"

    def save(self, *args, **kwargs):
        # Save the main image first
        super().save(*args, **kwargs)

        # Create thumbnail if it doesn't exist
        if self.image and not self.thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        try:
            img = Image.open(self.image.path)
            output_size = (300, 200)
            img.thumbnail(output_size)
            
            thumb_name = f"thumb_{self.image.name.split('/')[-1]}"
            thumb_path = os.path.join('thumbnails', thumb_name)
            
            # Save to media directory
            thumb_io = BytesIO()
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            img.save(thumb_io, format='JPEG', quality=85)
            self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)
            self.save()
        except Exception as e:
            print(f"Error creating thumbnail: {e}")

    def delete(self, *args, **kwargs):
        # Delete the image files when the model instance is deleted
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.thumbnail:
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)
        super().delete(*args, **kwargs)