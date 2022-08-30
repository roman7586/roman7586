import django_filters
from django.forms import DateInput
from django_filters import FilterSet

from .models import Otvet


class PostFilter(FilterSet):
    """Otvet_to = ModelChoiceFilter(
        queryset=get_post_title
    )"""
    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Otvet
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = {
            'text': ['icontains']

                  }