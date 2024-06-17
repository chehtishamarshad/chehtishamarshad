from django.urls import path #import views form main project urls 
from . import views  #import all views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:id>/', views.post_detail, name='post-detail'),
    path('post/new/', views.post_create, name='post-create'),
    path('post/<int:id>/update/', views.post_update, name='post-update'),
    path('post/<int:id>/delete/', views.post_delete, name='post-delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
]
