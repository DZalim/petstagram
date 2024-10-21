from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetAddForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet


class AddPetView(CreateView):
    model = Pet
    # queryset = Pet.objects.all() #This can also be submitted instead of model=Pet. Either one or the other. Not both for the base model
    form_class = PetAddForm
    template_name = 'pets/pet-add-page.html'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})  # pk=1 it will change after we create an account


class PetDetailsView(DetailView):  # DetailView cannot work with Forms. Does not inherit Form!!
    model = Pet
    template_name = 'pets/pet-details-page.html'
    slug_url_kwarg = 'pet_slug'  # <slug:pet_slug>

    def get_context_data(self, **kwargs):  # Because the photos and comments do not come with the Pet model
        context = super().get_context_data(**kwargs)
        context["all_photos"] = context["pet"].photo_set.all()
        context[
            "comment_form"] = CommentForm()  # This is for preview only. How it works - comment_functionality in common app

        return context


class PetEditView(UpdateView):
    model = Pet
    form_class = PetEditForm
    template_name = 'pets/pet-edit-page.html'
    slug_url_kwarg = 'pet_slug'

    def get_success_url(self):  # because the data comes dynamically for pet_slug and username
        return reverse_lazy(
            'pet-details',
            kwargs={
                'username': self.kwargs['username'],
                'pet_slug': self.kwargs['pet_slug']
            }
        )


class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'pets/pet-delete-page.html'
    form_class = PetDeleteForm
    slug_url_kwarg = 'pet_slug'
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def get_initial(self):  # Just populates the data. But the data is not submitted to the delete form
        return self.get_object().__dict__

    # We have both field.widget.attrs['readonly'] = True and field.widget.attrs['disabled'] = True
    # if only field.widget.attrs['readonly'] = True - only get_initial work.
    # But for field.widget.attrs['disabled'] = True - we need get_form_kwargs

    def get_form_kwargs(self):  # Submits the data to the delete form
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.get_initial()
        })

        return kwargs

# def add_pet(request):
#     form = PetAddForm(request.POST or None)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('profile-details', pk=1) # pk=1 it will change after we create an account
#
#     context = {
#         "form": form
#     }
#
#     return render(request, 'pets/pet-add-page.html', context=context)

# def show_pet_details(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     all_photos = pet.photo_set.all()
#     comment_form = CommentForm()
#
#     context = {
#         'pet': pet,
#         'all_photos': all_photos,
#         'comment_form': comment_form
#     }
#
#     return render(request, 'pets/pet-details-page.html', context)

# def edit_pet(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetEditForm(request.POST or None, instance=pet)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('pet-details', username, pet_slug)
#
#     context = {
#         "form": form,
#         "pet": pet
#     }
#
#     return render(request, 'pets/pet-edit-page.html', context)

# def delete_pet(request, username, pet_slug):
#     pet = Pet.objects.get(slug=pet_slug)
#     form = PetDeleteForm(instance=pet)
#
#     if request.method == "POST":
#         pet.delete()
#         return redirect('profile-details', pk=1)
#
#     context = {
#         "form": form,
#         "pet": pet,
#     }
#
#     return render(request, 'pets/pet-delete-page.html', context)
