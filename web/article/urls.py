from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('',views.home_page,name='home_page'),
    path('article/<int:id>/',views.article_page,name='article_page'),
    path('news_list/',views.news_list,name='news_list'),
    path('category_list/',views.category_list,name='category_list'),
    path('category/<str:id>/',views.category,name='category'),
    path('comment_post/<int:id>/',views.comment_post,name='comment_post'),
    path('comment_del/<int:id>/',views.comment_del,name='comment_del'),
    path('search/',views.search,name='search')
]