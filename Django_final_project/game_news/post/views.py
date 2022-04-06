
from django.shortcuts import render, get_object_or_404
from django.views import generic


from .models import Post, Comments
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse,reverse_lazy
from django.core.mail import send_mail
from .forms import CommentForm
from .filters import CommentsFilter


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    posts=Post.objects.all()
    users=User.objects.all() 
    return render(
        request,
        'index.html',
        context={'posts':posts,'users':users,},
    )


class UserPosts(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(authort=self.request.user)


class UserComments(LoginRequiredMixin,generic.ListView):
    model = Comments
    paginate_by = 5

    def get_queryset(self):
        return Comments.objects.filter(post__authort = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentsFilter(self.request.GET, queryset=self.get_queryset())  
        return context


def AddComment(request, pk):
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, pk=pk)

        
        commentss = post.comments_set.all()

        if form.is_valid():
            cooment = form.cleaned_data['cooment']

            comments = Comments.objects.create(
                cooment=cooment, post=post, author = request.user, status = False
            )

            form = CommentForm()
            send_mail( 
            subject=f'Отклики на {comments.post.title}',
            message=f'На вашь пост {comments.post.title} от {request.user} поступил отклик', 
            from_email='gavriloviy@mail.ru',
            recipient_list=[post.authort.email] 
            )
            return HttpResponseRedirect(reverse('index') )

        return render(request, 'post/add_comment.html', {'form': form, 'comments':commentss})



def append_comment(request, pk):
    try:
        comment = get_object_or_404(Comments, pk=pk)
        comment.status = True
        comment.save()
        send_mail( 
            subject=f'Ваш отзыв приняли',
            message=f'Пользователь {request.user} принял ваш отзыв на статью {comment.post}', 
            from_email='gavriloviy@mail.ru', 
            recipient_list=[comment.author.email]  
            )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        return HttpResponseNotFound("<h2>Comment not found</h2>")


def delete_commnet(request, pk):
    try:
        comment = get_object_or_404(Comments, pk=pk)
        comment.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        return HttpResponseNotFound("<h2>Comment not found</h2>")


class PostDetailView(LoginRequiredMixin,generic.DetailView):
    model = Post
    
    template_name = 'post/post_detail.html'


class PostCreate(LoginRequiredMixin,generic.edit.CreateView):
    model = Post
    fields = ['title', 'type_post', 'text', 'upload']

    def form_valid(self, form):
        form.instance.authort = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostUpdate(LoginRequiredMixin,generic.edit.UpdateView):
    model = Post
    fields = '__all__'


class PostDelete(LoginRequiredMixin,generic.edit.DeleteView):
    model = Post
    success_url = reverse_lazy('my-posts')


class CommentCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Comments
    fields = '__all__'