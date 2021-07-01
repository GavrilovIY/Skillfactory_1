from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['post_author_rating', 'selection_field',
                  'category', 'title', 'text']

