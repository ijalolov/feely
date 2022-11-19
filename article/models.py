from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, related_name='articles', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    body = RichTextUploadingField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at', 'id']
        db_table = 'article'


class Adv(models.Model):
    link = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return str(self.link)

    @classmethod
    def get_solo(cls):
        obj = cls.objects.last()
        if not obj:
            obj = cls.objects.create()
        return obj

    class Meta:
        verbose_name = 'Adv'
        verbose_name_plural = 'Adv'


class AdvImage(models.Model):
    adv = models.ForeignKey(Adv, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
