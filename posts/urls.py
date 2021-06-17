from django.contrib.auth import views as auth_views
from .views import *
from . import views
from django.urls import path

urlpatterns = [
	path('', views.index, name='index'),
	path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('allPosts', allPosts, name = 'allPosts'),    
    path("addThanks", views.addThanks, name='addThanks'),
    path('editProfile', views.editProfile , name='editProfile'),
    path("<int:id>", views.profile, name='profile'),
    path('journal', views.journal, name='journal'),
    path("edit/<int:post_id>", views.editView, name='editView'),
    path("updatefollow/<int:id>", views.update_follow, name='update_follow'),
    path('following', views.following, name='following'),
    path("like", views.like_post, name='like_post'),
    path("maps", views.maps, name="maps"),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name = "registration/reset_password.html"), name="reset_password"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),  name="password_reset_confirm"), 
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_reset_complete.html"), name="password_reset_complete")
]