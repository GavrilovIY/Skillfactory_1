from django_filters import FilterSet

from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = ('post_author_rating__user__username', 'time_add')