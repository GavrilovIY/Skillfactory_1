from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):




class Category(models.Model):
    news_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    paper = 'PA'
    news = 'NE'
    PUBLICATION = [
        (paper, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author)
    selection_field = models.CharField(max_length=2, choices = PUBLICATION, default=news)
    time_add = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField()

    def preview(self):
        return self.text[0:123]+'...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



class PostCategory(models.Model):
    post = models.OneToOneField(Post)
    Category = models.OneToOneField(Category)


class Comment(models.Model):
    post = models.OneToOneField(Post)
    user = models.OneToOneField(User)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices = POSITIONS, default = cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        array_name = self.full_name.split()
        return array_name[0]


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")




class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            seconds = (self.time_out - self.time_in).total_seconds()
            return seconds//60
        else:
            seconds = (datetime.now() - self.time_in).total_seconds()
            return seconds//60


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1)


    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def propduct_sum(self):
        product_price = self.product.price
        return product_price*self.amount

