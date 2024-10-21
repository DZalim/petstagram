from django.core.paginator import Paginator
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


class HomeView(ListView):  # ListView does not inherit Form
    model = Photo
    template_name = 'common/home-page.html'
    context_object_name = 'all_photos'  # by default is object_list => photos
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comment_form'] = CommentForm()
        context['search_form'] = SearchForm(self.request.GET)  # self.request.GET so that what is written in the search engine remains and does not disappear
        context['all_photos'] = context['page_obj']  # paginator paje obg

        return context

    def get_queryset(self):
        queryset = super().get_queryset()  # All objects
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(
                tagged_pets__name__icontains=pet_name
            )

        return queryset


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


def comment_functionality(request, photo_id: int):
    if request.POST:
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)  # to add a relation in the following rows
            comment.to_photo = photo
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')

# def home(request):
#     all_photos = Photo.objects.all().order_by('id')
#     comment_form = CommentForm()
#     search_form = SearchForm(request.GET)
#
#     if search_form.is_valid():
#         all_photos = all_photos.filter(
#             tagged_pets__name__icontains=search_form.cleaned_data['pet_name']
#         )
#
#     photos_per_page = 1
#     paginator = Paginator(all_photos, photos_per_page)
#     page_number = request.GET.get('page')  # http://localhost:8000/?page=10 => GET {"page": 10}
#
#     all_photos = paginator.get_page(page_number) # page_obj
#
#     context = {
#         "all_photos": all_photos,
#         "comment_form": comment_form,
#         "search_form": search_form
#     }
#
#     return render(request, 'common/home-page.html', context=context)
