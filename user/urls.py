from django.urls import path

from user import views

urlpatterns = [
   path('', views.UserListView.as_view(), name='users'),
   path("<int:pk>/update/", views.UserUpdateView.as_view(), name="update_user"),
   path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete_user"),
   path('<int:pk>/', views.UserDetailView.as_view(), name='detail_user'),
   path('create/', views.UserCreateView.as_view(), name='create_user'),
]
