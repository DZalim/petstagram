from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.pets.models import Pet
from petstagram.photos.validators import FileSizeValidator

UserModel = get_user_model()


# Create your models here.
class Photo(models.Model):
    photo = models.ImageField(
        upload_to='',
        validators=[
            FileSizeValidator(5),
        ],
    )  # To work with an image field, we should install a library called Pillow: pip install Pillow
    description = models.TextField(
        max_length=300,
        validators=[
            MinLengthValidator(10),
        ],
        blank=True,
        null=True
    )
    location = models.CharField(max_length=30, blank=True, null=True)
    tagged_pets = models.ManyToManyField(Pet, blank=True)
    date_of_publication = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
