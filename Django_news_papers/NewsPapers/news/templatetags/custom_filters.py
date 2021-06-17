from django import template

register = template.Library()


@register.filter(name='censour')
def censour(value, arg):
    for word in arg.split(','):
        word = word.lower()
        for text_word in value.split(' '):
            text_word = text_word.lower()
            if text_word == word:
                return 'В тексте содержится не цензурная лексика'
    return value