import datetime
import os
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


def validate_file_extension(value):
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extension = ['.png', '.jpg']
    if not ext in valid_extension:
        raise ValidationError('Unsupported extension')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatar/', blank=False, null=False, validators=[validate_file_extension])
    description = models.CharField(max_length=512, null=False, blank=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Article(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    cover = models.FileField(upload_to='files/article_cover/', null=False, blank=False, validators=[validate_file_extension])
    content = RichTextField()
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    promote = models.BooleanField(default=False)

class Category(models.Model):
    title = models.CharField(max_length=120, blank=False, null=False)
    cover = models.FileField(upload_to='files/category_cover/', blank=False, null=False, validators=[validate_file_extension])

    def __str__(self):
        return self.title