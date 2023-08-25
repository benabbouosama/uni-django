from django import forms
from .models import Level , News

class LevelSelectForm(forms.Form):
    levels = forms.ModelChoiceField(queryset=Level.objects.all(), empty_label=None)

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'pdf']