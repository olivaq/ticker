from django import template
register = template.Library()

from collections import Iterable

@register.filter
def iterable(value):
	"""
	Return true if iterable
	"""
	return isinstance(value, Iterable)
