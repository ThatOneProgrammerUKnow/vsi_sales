from django_tables2.views import SingleTableView

class BaseSessionViewMixin:
    menu_slug = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_slug"] = self.menu_slug
        return context

class SingleTableViewBase(SingleTableView):
    object_list = None

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        return super().get_context_data(**kwargs)