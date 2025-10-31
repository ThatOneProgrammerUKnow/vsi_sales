from django.views.generic import TemplateView

class BaseSessionView(TemplateView):
    menu_slug = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_slug"] = self.menu_slug
        return context
