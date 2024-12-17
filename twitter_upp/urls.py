from django.contrib import admin
from django.urls import path, include
from posts import views as post_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True), 
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('posts/', include('posts.urls')),
]
