
# How we render forms in templates
See the templats in `templates/forms` and see `apps/accounts/templatetags/form_tags.py`.

Django forms should be rendered using the "render_form_fields" and/or "render_field" form tags. These template tags uses the predefined templates to render each form field. To use this, add this to the top of your template:

```
{% load form_tags %}
```

This makes `render_form_fields` and `render_field` available in the template.

## Usage of these template variables
Assume the form is available in the template as `form`

### Render all fields on the form
```
{% render_form_fields form %}
```

### Render certain form fields
```
{% render_form_fields form "login" "password" "remember" %}
```

### Render a field and add attributes to its element
```
{% render_field form.your_field attr1="value1" %}
```



