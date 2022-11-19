from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='images/')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'id']
        db_table = 'category'


class Specialization(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'
        db_table = 'specialization'


class Doctor(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='doctor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='doctors')
    specializations = models.ManyToManyField(Specialization, related_name='doctors')
    company = models.CharField(max_length=255, blank=True, null=True)
    about = RichTextUploadingField()
    youtube_link = models.URLField(null=True, blank=True)
    hour_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Sum')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        db_table = 'doctor'


class DoctorRating(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='doctor_ratings')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.doctor)

    class Meta:
        verbose_name = 'Doctor Rating'
        verbose_name_plural = 'Doctor Ratings'
        db_table = 'doctor_rating'
        unique_together = ('doctor', 'user')


class VideoCourseCategory(models.Model):
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video Course Category'
        verbose_name_plural = 'Video Course Categories'
        ordering = ['order', 'id']
        db_table = 'video_course_category'


class VideoCourse(models.Model):
    category = models.ForeignKey(VideoCourseCategory, on_delete=models.CASCADE, related_name='video_courses', null=True)
    title = models.CharField(max_length=1024)
    youtube_link = models.URLField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video Course'
        verbose_name_plural = 'Video Courses'
        db_table = 'video_course'
        ordering = ['order', 'id']
