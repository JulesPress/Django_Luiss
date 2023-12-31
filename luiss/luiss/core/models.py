from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Product(models.Model):
    DRAFT = "draft"
    WAITING_APPROVAL = "waitingapproval"
    ACTIVE = "active"
    DELETED = "deleted"

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting Approval'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="uploads/product_images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/product_images/thumbnail', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'


    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail





