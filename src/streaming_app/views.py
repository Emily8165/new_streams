from django.views import generic

from . import models


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "home.html"
    title = "home"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context


class ListAllSongs(generic.ListView):
    template_name = "list_of_songs.html"
    title = "list of songs"
    model = models.Song
    fields = [
        field
        for field in models.Song._meta.get_fields()
        if field.verbose_name != "meta data"
    ]

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["model"] = self.model.objects.all()
        context["fields"] = self.fields
        return context


class SongMetaDataView(generic.DetailView):
    template_name = "song_meta_data.html"
    title = "Song Meta Data"
    model = models.ListenerMetaData
