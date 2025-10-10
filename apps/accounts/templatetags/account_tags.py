from django import template

register = template.Library()


@register.filter
def is_menu_active(selected_menu_slug, menu_slug):
    if selected_menu_slug == menu_slug:
        return "active"
    return ""
