from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_author.aggregate(postRating = Sum('post_rating'))
        auth_comRat = self.user.com_user.aggregate(comRating = Sum('comment_rating'))
        post_authRat = self.post_author.all().aggregate(authRating = Sum('com_post__comment_rating'))
        if not auth_comRat.get('comRating'):
            self.user_rating = postRat.get('postRating') * 3 + post_authRat.get('authRating')
        elif not post_authRat.get('authRating'):
            self.user_rating = postRat.get('postRating') * 3 + auth_comRat.get('comRating')
        else:
            self.user_rating = postRat.get('postRating') * 3 + auth_comRat.get('comRating') + post_authRat.get(
                'authRating')
        self.save()


class Category(models.Model):
    news_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    paper = 'PA'
    news = 'NE'
    PUBLICATION = [
        (paper, 'Статья'),
        (news, 'Новость')
    ]
    post_author_rating = models.ForeignKey(Author, related_name='post_author',on_delete=models.CASCADE)
    selection_field = models.CharField(max_length=2, choices = PUBLICATION, default=news)
    time_add = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='NewPaper')
    text = models.TextField(default='FreeToAdd')
    post_rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[0:123]+'...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, related_name='com_post', on_delete=models.CASCADE, null=True)
    comment_user = models.ForeignKey(User, related_name='com_user', on_delete=models.CASCADE, null=True)
    text = models.TextField(default='FreeToAdd')
    time_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()