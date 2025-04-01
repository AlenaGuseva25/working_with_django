from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    preview_image = models.ImageField(upload_to="blog_preview/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)


    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = "Блоговые записи"
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
            ('can_delete_blog', 'Can delete blog')
        ]

    def __str__(self):
        return self.title

