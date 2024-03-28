from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, SecurityFeature, TechSecurityItem


class CommentForm(forms.ModelForm):
    """ Create Comment Form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """Get comment model, choose fields to display"""
        model = Comment
        fields = ('body',)


class SecurityFeatureForm(forms.ModelForm):
    """ Create security feature Form """
    def __init__(self, *args, **kwargs):
        super(SecurityFeatureForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """
        Get security feature model,
        choose fields to display and add summernote widget
        """
        model = SecurityFeature
        fields = [
            'title',
            'description',
            'method',
            'image',
            'status',
        ]
        widgets = {
            'method': SummernoteWidget(),
        }


class TechSecurityForm(forms.ModelForm):
    """ Create tech security Form """
    class Meta:
        """Get tech security model, choose fields to display"""
        model = TechSecurityItem
        fields = ('day',)
