from django.views import generic


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "home.html"
    title = "home"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        return context
