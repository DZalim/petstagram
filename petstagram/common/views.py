from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.models import Like
from petstagram.photos.models import Photo


# Create your views here.
def home(request):
    all_photos = Photo.objects.all()

    context = {
        "all_photos": all_photos
    }

    return render(request, 'common/home-page.html', context=context)


def like_functionality(request, photo_id):
    liked_object = Like.objects.filter(to_photo_id=photo_id).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_photo_id=photo_id)
        like.save()

    # redirect to the last visited page (request.META['HTTP_REFERER']) and will stop exactly at the photo we liked/unliked (f'#{photo_id}')
    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


def share_functionality(request, photo_id):  # copy_link_to_clipboard

    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))
    # HTTP_HOST = http://127.0.0.1/ + resolve_url= photos/int:pk/

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')
