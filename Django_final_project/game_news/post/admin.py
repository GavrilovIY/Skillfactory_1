from django.contrib import admin
from .models import Post, Comments
from django.contrib.auth.models import User


admin.site.register(Post)
admin.site.register(Comments)
