from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib import messages

def home(request):
    """
    Vista principal (Home): Lista todos los posts ordenados por los más recientes.
    """
    posts = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        liked_posts = []

    return render(request, 'posts/home.html', {
        'posts': posts,
        'liked_posts': liked_posts,
    })

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'posts/profile.html', {'posts': posts})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    messages.success(request, "¡Tu post ha sido eliminado!")
    return redirect('profile')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, "¡Tu post ha sido editado con éxito!")
            return redirect('profile')
    return render(request, 'posts/edit_post.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(user=request.user, title=title, content=content)
            messages.success(request, "¡Tu post ha sido publicado!")
            return redirect('home')
        else:
            messages.error(request, "Debes ingresar un título y contenido.")
    return render(request, 'posts/create_post.html')

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        messages.info(request, "Has quitado tu like.")
    else:
        post.likes.add(request.user)
        messages.success(request, "Has dado like al post.")
    
    post.save()
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu cuenta ha sido creada! Ahora puedes iniciar sesión.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})
