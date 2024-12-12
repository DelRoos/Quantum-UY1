from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import Post
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm, PostForm
from django.conf import settings
from django.contrib.auth import get_user_model
from members.models import Profile


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'modèle/blog/affichage_articles.html'


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 2)
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
        {'posts': posts, 'comments_dict': comments_dict, 'paginator': paginator}
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
    
    author = post.author
    posts_author = Post.published.filter(author=author).exclude(id=post.id)
    try:
        author_profile = Profile.objects.get(user=author)
    except Profile.DoesNotExist:
        author_profile = None

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'author': author,
        'posts_author': posts_author,
        'author_profile': author_profile,
        'comment': comment  
    }
    return render(request, 'modèle/blog/article.html', context)



def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect('blog:create_post')
    else:
        form = PostForm()
    
    return render(request, 'modèle/blog/create_post.html', {'form': form})