from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from petstagram.photos.models import Photo


class PhotoAddView(CreateView):
    model = Photo
    template_name = 'photos/photo-add-page.html'
    form_class = PhotoAddForm
    success_url = reverse_lazy('home')


class PhotoDetailsView(DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['likes'] = self.object.like_set.all()
        context['comments'] = self.object.comment_set.all()
        context['comment_form'] = CommentForm()

        return context


class PhotoEditView(UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('photo-details',
                            kwargs={'pk': self.object.pk})


def delete_photo(request, pk):
    Photo.objects.get(pk=pk).delete()
    return redirect('home')

# def add_photo(request):
#     form = PhotoAddForm(request.POST or None, request.FILES or None)
#
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'photos/photo-add-page.html', context)

# def edit_photo(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     form = PhotoEditForm(request.POST or None, instance=photo)  # we don't have request.FILES because we don't send the photo with a form
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('photo-details', pk)
#
#     context = {
#         "form": form,
#         "photo": photo
#     }
#
#     return render(request, 'photos/photo-edit-page.html', context)

# def show_photo_details(request, pk):
#     photo = Photo.objects.get(pk=pk)
#     likes = photo.like_set.all()
#     comments = photo.comment_set.all()
#
#     comment_form = CommentForm()
#
#     context = {
#         'photo': photo,
#         'likes': likes,
#         'comments': comments,
#         'comment_form': comment_form,
#     }
#
#     return render(request, 'photos/photo-details-page.html', context)
