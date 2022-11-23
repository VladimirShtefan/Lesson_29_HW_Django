from django.urls import path

from ad import views

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad'),
    path('create/', views.AdCreateView.as_view(), name='create_ad'),
    path("<int:pk>/update/", views.AdUpdateView.as_view(), name="update_ad"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(), name="delete_ad"),
    path("<int:pk>/image/", views.AdImageView.as_view(), name="add_image_ad"),
    path('<int:pk>/', views.AdDetailView.as_view(), name='detail_ad'),
]
