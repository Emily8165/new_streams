from django import http
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "home.html"
    title = "Home"
    user = models.Listener.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "logout" in request.GET:
            try:
                logged_in_user = models.Listener.objects.get(is_active=True)
                logged_in_user.is_active = False
                logged_in_user.save()
            except models.Listener.DoesNotExist:
                pass
            return self.render_to_response(context)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["user"] = self.user if self.user else ""
        return context


class ListAllSongs(generic.ListView):
    template_name = "list_of_songs.html"
    title = "List of Songs"
    model = models.Song
    fields = [field for field in models.Song._meta.get_fields() if field != "meta_data"]

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["model"] = self.model.objects.all()
        context["fields"] = self.fields
        return context


class LoginView(generic.FormView):
    template_name = "login.html"
    title = "Log Into Streams"
    form_class = forms.LoginForm
    success_url = reverse_lazy("home")
    errors = []

    def form_valid(self, form):
        try:
            listener = models.Listener.objects.get(
                Q(email=form.cleaned_data["email"]) | Q(name=form.cleaned_data["name"])
            )
        except models.Listener.DoesNotExist:
            self.errors.append(
                "That name or email could not be found! Please try again"
            )
            return http.HttpResponseRedirect(redirect_to=reverse_lazy("login"))
        if form.cleaned_data["password"] == listener.password:
            listener.is_active = True
            listener.save()
            return super().form_valid(form)
        else:
            self.errors.append("That is not the right password!")
            return http.HttpResponseRedirect(redirect_to=reverse_lazy("login"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["form"] = self.form_class
        context["errors"] = self.errors
        return context


class SongMetaDataView(generic.DetailView):
    template_name = "song_meta_data.html"
    title = "Song Meta Data"
