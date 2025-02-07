from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import Categorie, Post
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm, PostForm
from django.conf import settings
from django.contrib.auth import get_user_model
from members.models import Profile
from taggit.models import Tag
from django.db.models import Count
import markdown2
from django.utils.html import mark_safe


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'modèle/blog/listing.html'



def post_list(request):
    posts = Post.published.all()
    selected_categories = request.GET.get('categories', '')  # Récupérer les catégories sélectionnées
    selected_categories_list = selected_categories.split(',') if selected_categories else []

    if selected_categories_list:
        posts = posts.filter(categorie__name__in=selected_categories_list).distinct()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    all_categories = Categorie.objects.all()
    article = Post.published.order_by('publish')[:3]
    return render(
        request,
        'modèle/blog/listing.html',
        {
            'posts': posts,
            'selected_categories': selected_categories_list,
            'all_categories': all_categories,
            'paginator': paginator,
            'article': article,
        }
    )

def listing(request):
    posts = Post.published.all()
    selected_categories = request.GET.get('categories', '')  # Récupérer les catégories sélectionnées
    selected_categories_list = selected_categories.split(',') if selected_categories else []

    if selected_categories_list:
        posts = posts.filter(categorie__name__in=selected_categories_list).distinct()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    all_categories = Categorie.objects.all()
    article = Post.published.order_by('publish')[:3]
    return render(
        request,
        'modèle/blog/affichage_articles.html',
        {
            'posts': posts,
            'selected_categories': selected_categories_list,
            'all_categories': all_categories,
            'paginator': paginator,
            'article': article,
        }
    )





def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
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

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    html_content = markdown2.markdown(post.body, extras=["tables", "fenced-code-blocks"])
    
    post.body_html = mark_safe(html_content)
    
    



    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'author': author,
        'posts_author': posts_author,
        'author_profile': author_profile,
        'comment': comment,  
        'similar_posts': similar_posts
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