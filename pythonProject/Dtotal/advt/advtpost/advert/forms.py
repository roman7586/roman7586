from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .models import Post, Otvet, NewsMail


class PostForm(forms.ModelForm): # Форма создания обьявления
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
            'content'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        author_group = Group.objects.get(name='author')
        author_group.user_set.add(user)
        return user

class OtclickForm(forms.ModelForm): # Форма отклика
    class Meta:
        model = Otvet
        fields = ['text',]

class NewsForm(forms.ModelForm): # Форма для рассылки новостей
    class Meta:
        model = NewsMail
        fields = ['title', 'text']