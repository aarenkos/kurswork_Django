from django.db import models
from PIL import Image

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(max_length=400, verbose_name='содержание', **NULLABLE)
    picture = models.ImageField(default='place_holder.png', upload_to='blog_images/', verbose_name='изображение', **NULLABLE)
    view_counter = models.IntegerField(default=0, verbose_name='количество просмотров')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.picture:
            image = Image.open(self.picture.path)
            target_size = (300, 300)
            image.thumbnail(target_size)
            image.save(self.picture.path)