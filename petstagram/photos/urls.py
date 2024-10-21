from django.urls import path, include
from petstagram.photos import views


urlpatterns= [
    path('add', views.PhotoAddView.as_view(), name='add-photo'),
    path('<int:pk>/', include([
        path('', views.PhotoDetailsView.as_view(), name='photo-details'),
        path('edit/', views.PhotoEditView.as_view(), name='photo-edit'),
        path('delete/', views.delete_photo, name='photo-delete')
    ]))
]

# urlpatterns= [
#     path('add', views.add_photo, name='add-photo'),
#     path('<int:pk>/', include([
#         path('', views.show_photo_details, name='photo-details'),
#         path('edit/', views.edit_photo, name='photo-edit'),
#         path('delete/', views.delete_photo, name='photo-delete')
#     ]))
# ]