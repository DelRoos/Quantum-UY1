from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import Post
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm, PostForm
from django.conf import settings
from django.contrib.auth import get_user_model


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    comments_dict = {}
    for post in posts:
        comments_dict[post.id] = post.comments.filter(active=True)


    return render(
        request,
        'modèle/blog/affichage_articles.html',
        {'post_list': post_list, 'comments_dict': comments_dict}
    )

def post_detail(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED
    )
    comments = post.comments.filter(active=True)[:3]

    form = CommentForm(request.POST if request.method == 'POST' else None)

    comment = None
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        form = CommentForm()  
    
    User = get_user_model()
    author = get_object_or_404(User, id=id)
    posts_author = Post.published.filter(author=author).exclude(id=post.id)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'author': author,
        'posts_author': posts_author,
        'comment': comment  
    }
    return render(request, 'modèle/blog/article.html', context)



def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    
    return render(request, 'modèle/blog/create_post.html', {'form': form})