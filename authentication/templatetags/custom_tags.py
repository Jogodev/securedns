from django import template

register = template.Library()

@register.filter
def add_attrs(field, attrs):
    """Add css attributes"""
    attrs_dict = {}
    for attr in attrs.split(","):
        if "=" in attr:  # Vérifier la présence de '='
            key, value = attr.split("=", 1)
            attrs_dict[key.strip()] = value.strip()
        else:
            # Ajouter les classes dans "class"
            attrs_dict["class"] = attrs_dict.get("class", "") + " " + attr.strip()
    return field.as_widget(attrs=attrs_dict)