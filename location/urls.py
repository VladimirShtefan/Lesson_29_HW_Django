from django.urls import path

from location import views


urlpatterns = [
   path('', views.LocationListView.as_view(), name='locations'),
   path('<int:pk>/', views.LocationDetailView.as_view(), name='detail_location'),
   path('create/', views.LocationCreateView.as_view(), name='create_location'),
]
