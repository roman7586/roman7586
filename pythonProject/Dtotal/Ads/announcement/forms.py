from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
            'content',
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

#Добавление в группы при регистрации
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='author')
        common_group.user_set.add(user)
        return user