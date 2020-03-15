from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['body'].label = ''
        
# class SubCommentForm(forms.ModelForm):
#     class Meta:
#         model = SubComment
#         fields = ('body',)
    
#     def __init__(self, *args, **kwargs):
#         super(SubCommentForm, self).__init__(*args, **kwargs)
#         self.fields['body'].label = ''

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = 'Repeat password'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ""