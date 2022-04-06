from dataclasses import fields
import django_filters
from .models import Comments, Post


class CommentsFilter(django_filters.FilterSet):
    
    class Meta():
        model = Comments
        fields={'post'}

   