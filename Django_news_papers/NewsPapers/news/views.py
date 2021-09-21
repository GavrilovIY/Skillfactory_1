from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, \
    DeleteView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core.cache import cache

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, User

import datetime

import logging

logger = logging.getLogger(__name__)




class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-time_add')
    paginate_by = 10


class CategoryList(PermissionRequiredMixin, ListView):
    model = Category
    template_name = 'categories.html'
    permission_required = 'news.change_category'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['is_category'] = context['categories'].filter(subscribers=self.request.user)
        for i in context['categories']:
            if i not in context['is_category']:
                print(i)
        return context




class CategoryDetail(PermissionRequiredMixin, DetailView):
    model = Category
    template_name = 'category_sub.html'
    permission_required = 'news.view_category'
    context_object_name = 'category_sub'

    def get_object(self, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        print(id)
        category = Category.objects.get(pk=id)

        for i in Category.objects.all():
            if i not in Category.objects.all().filter(subscribers=user):
                category.subscribers.add(user)

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}',obj)

        return obj


class PostSearch(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news_search'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/news_create.html'
    permission_required = ('news.add_post',)
    form_class = PostForm

    # def post(self, request, *args, **kwargs):
    #     category_list = Category.objects.filter(id__in=request.POST.getlist('category')).values('subscribers')
    #     user_list = User.objects.filter(id__in=category_list)
    #     email_list = [i.get('email') for i in user_list.values('email')]
    #     for i in user_list:
    #         html_content = render_to_string(
    #             'news/send_notify.html',
    #             {
    #                 'post_text': request.POST['text'][:50],
    #                 'username': i.username,
    #             }
    #         )
    #         email_text = EmailMultiAlternatives(
    #             subject=request.POST['title'],
    #             body='text',
    #             to=[i.email],
    #         )
    #         email_text.attach_alternative(html_content, "text/html")
    #         email_text.send()
    #     return super().post(request, *args, **kwargs)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news/news_create.html'
    permission_required = ('news.change_post',)
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):

    template_name = 'news/news_delete.html'
    context_object_name = 'new'
    queryset = Post.objects.all()
    success_url = '/news/'
