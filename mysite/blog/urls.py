from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [

    path('list_blog/', views.post_list, name='post_list'),
    # path('list_blog/', views.PostListView.as_view(), name='post_list'),
    path(
        'list_blog/<int:id>/',
        views.post_detail,
        name='post_detail'
    ),
    path('create/', views.create_post, name='create_post'),
]
