from django.core.exceptions import PermissionDenied
from django.utils.functional import SimpleLazyObject

from apps.accounts.models.account_models import GroupUser


class CustomMiddlewareMixin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class GroupMembershipRequiredMiddleware(CustomMiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        if group_slug := view_kwargs.get("group_slug"):
            group_user_query = GroupUser.objects.filter(
                invite_accepted=True, group__slug=group_slug, user=user
            )
            if not group_user_query.exists():
                raise PermissionDenied()

            request.group_user = SimpleLazyObject(lambda: group_user_query.first())
