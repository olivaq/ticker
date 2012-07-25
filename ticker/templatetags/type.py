from django import template
register = template.Library()

from collections import Iterable

@register.filter(name="type")
def dtype(value):
	"""
	Return true if iterable
	"""
	return type(value).__name__
