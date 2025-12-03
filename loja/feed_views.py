from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import FeedPost


def feed_list(request):
    """Lista todos os posts publicados do feed"""
    now = timezone.now()
    
    # Busca posts publicados e cuja data de agendamento já passou
    posts = FeedPost.objects.filter(
        is_published=True,
        scheduled_date__lte=now
    ).order_by('-scheduled_date')
    
    return render(request, 'feed_list.html', {
        'posts': posts
    })


def feed_detail(request, pk):
    """Exibe detalhes de um post específico"""
    now = timezone.now()
    
    # Busca post publicado
    post = get_object_or_404(
        FeedPost,
        pk=pk,
        is_published=True,
        scheduled_date__lte=now
    )
    
    return render(request, 'feed_detail.html', {
        'post': post
    })
