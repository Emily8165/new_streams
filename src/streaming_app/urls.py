from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("list/", views.ListAllSongs.as_view(), name="list_songs"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("list/<int:pk>/", views.SongMetaDataView.as_view(), name="meta_data"),
]
