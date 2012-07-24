from django import forms
from django.forms import ModelForm
from models import Node
"""
class NodeForm(forms.Form):
    title = forms.CharField(max_length=255)
    code = forms.Textarea()
    enabled = forms.BooleanField(required=False)
    """

class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = ('code',)
"""
class PartialAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'title')
      """
