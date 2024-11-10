from django import forms

from petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ("user", )


class PhotoAddForm(PhotoBaseForm):
    pass


class PhotoEditForm(forms.ModelForm): # we do not inherit because there is another meta
    class Meta:
        model = Photo
        exclude = ['photo']


class PhotoDeleteForm(PhotoBaseForm):
    pass
