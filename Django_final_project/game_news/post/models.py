from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    TYPE_CATEGORY = (
        ('t', 'Tanks'),
        ('h', 'Hils'),
        ('d','DD'),
        ('t', 'Traders'),
        ('g', 'Guildmasters'),
        ('q','Questgivers'),
        ('b','Blacksmiths'),
        ('l','Leatherworkers'),
        ('p','Potions'),
        ('s', 'Spell masters'),
    )
    title = models.CharField(max_length=255)
    type_post = models.CharField(max_length=1,choices=TYPE_CATEGORY)
    text = models.TextField()
    data = models.DateField(auto_now_add=True)
    authort = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='upload/')  

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])


class Comments(models.Model):
    cooment = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)   

    class Meta:
        ordering = ('-date',)

    def __str__(self) -> str:
        return f'id {self.pk} author {self.author}'

    def get_absolute_url(self):
        return reverse('cooment-detail', args=[str(self.id)])
