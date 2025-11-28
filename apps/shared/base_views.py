from django_tables2.views import SingleTableView

class BaseSessionViewMixin:
    menu_slug = ""
    title_slug = ""
    button_slug = ""
    cancel_url = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_slug"] = self.menu_slug
        context["title_slug"] = self.title_slug
        context["button_slug"] = self.button_slug
        context["cancel_url"] = self.cancel_url
        return context

