from django import template
register = template.Library()

@register.filter(name='verbose_name')
def verbose_name(value):
	return value._meta.verbose_name

@register.filter(name='verbose_name_plural')
def verbose_name_plural(value):
	return value._meta.verbose_name_plural

@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

