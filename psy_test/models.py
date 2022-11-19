from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Test(models.Model):
    question = RichTextUploadingField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['order', 'id']


class TestOption(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='options')
    option = RichTextUploadingField()

    def __str__(self):
        return self.option
