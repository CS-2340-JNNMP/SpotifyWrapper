from django import forms

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),

        }
        labels = {}
