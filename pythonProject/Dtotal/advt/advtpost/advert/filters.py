import django_filters
from django.forms import DateInput
from django_filters import FilterSet

from .models import Otvet


class PostFilter(FilterSet):

    # dateCreation = django_filters.DateFilter(
    #     lookup_expr='gt',
    #     widget=DateInput(
    #         attrs={
    #             'type': 'date'
    #         }
    #     )
    # )
    class Meta:
        # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Otvet
        # В fields мы описываем по каким полям модели будет производиться фильтрация.
        fields = ['Otvet_to']
            # поиск по названию
            #'Otvet_to': ['icontains'],
            #'author__authorUser__username': ['icontains'],
