from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
import requests
from .models import (
    Post, Profile, PostView, Like, ProfileComment,
    Notification, PostImage, ContactMessage, Tag
)
from .forms import UserRegisterForm, ProfileUpdateForm
from .tasks import send_telegram_message_task



def send_telegram_message(name, message):
    token = "8158981655:AAGKDWbWL38fIHOFG3IPYP99EYuDPkEbZNs"
    chat_id = "6142181676"
    text = f"📩 Yangi xabar!\n\nKimdan: {name}\nXabar: {message}"
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': text,
    }

    try:
        response = requests.post(url, data=payload)
        print(f"Telegram status code: {response.status_code}")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")



def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


def post_detail(request, pk):
    # 1. Postni ID (pk) bo'yicha bazadan qidirib topadi
    post = get_object_or_404(Post, pk=pk)

    # 2. IP manzilni aniqlash (Mehmonlar uchun)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # 3. Ko'rishlar sonini qayd etish
    if request.user.is_authenticated:
        # Agar foydalanuvchi tizimga kirgan bo'lsa, uning nomi bilan saqlaydi
        PostView.objects.get_or_create(post=post, user=request.user)
    else:
        # Agar mehmon bo'lsa, IP manzili orqali saqlaydi
        PostView.objects.get_or_create(post=post, viewer_ip=ip)

    # 4. SIZ SO'RAGAN QATOR: Oxirgi o'qigan foydalanuvchilarni olish
    # Bu yerda user__isnull=False sharti faqat ro'yxatdan o'tganlarni saralab oladi
    readers = post.views.filter(user__isnull=False).select_related('user', 'user__profile').order_by('-viewed_at')[:10]

    # 5. Boshqa ma'lumotlar (Layklar, o'xshash postlar va h.k.)
    v_count = post.views.count()
    post_images = post.images.all()

    context = {
        'post': post,
        'post_images': post_images,
        'views_count': v_count,
        'readers': readers,  # HTML shablonga yuboriladigan o'zgaruvchi
    }

    return render(request, 'post_detail.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hisob yaratildi: {username}!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if request.FILES.get('avatar'):
            user_profile.avatar = request.FILES.get('avatar')
        if request.POST.get('bio'):
            user_profile.bio = request.POST.get('bio')
        user_profile.save()
        return redirect('profile')

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    total_views = PostView.objects.filter(post__author=request.user).count()
    comments = user_profile.comments.all().order_by('-created_at')

    return render(request, 'profile.html', {
        'user_posts': user_posts,
        'profile': user_profile,
        'total_views': total_views,
        'comments': comments,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'p_form': p_form})


def user_public_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    user_profile, created = Profile.objects.get_or_create(user=target_user)

    if request.method == "POST" and request.user.is_authenticated:
        comment_text = request.POST.get('comment_text')
        if comment_text:
            ProfileComment.objects.create(
                profile=user_profile,
                author=request.user,
                text=comment_text
            )
        return redirect('user_public_profile', username=username)

    comments = user_profile.comments.all().order_by('-created_at')
    user_posts = Post.objects.filter(author=target_user).order_by('-created_at')

    return render(request, 'user_public_profile.html', {
        'target_user': target_user,
        'profile': user_profile,
        'comments': comments,
        'user_posts': user_posts,
    })


@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(author=request.user, title=title, content=content)
        images = request.FILES.getlist('images')
        for img in images:
            PostImage.objects.create(post=post, image=img)
        messages.success(request, "Post muvaffaqiyatli yaratildi!")
        return redirect('home')
    return render(request, 'create_post.html')


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Siz faqat o'z postingizni tahrirlay olasiz!")

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        new_images = request.FILES.getlist('images')
        if new_images:
            for img in new_images:
                PostImage.objects.create(post=post, image=img)

        messages.success(request, "Post yangilandi!")
        return redirect('post_detail', pk=post.pk)
    return render(request, 'edit_post.html', {'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        post.delete()
        messages.warning(request, "Post o'chirildi.")
        return redirect('profile')
    return render(request, 'delete_confirm.html', {'post': post})


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reaction = request.GET.get('type', 'like')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    user = request.user if request.user.is_authenticated else None
    like_filter = Like.objects.filter(post=post, user=user, ip_address=ip)

    if like_filter.exists():
        old_reaction = like_filter.first()
        if old_reaction.reaction_type == reaction:
            like_filter.delete()
        else:
            old_reaction.reaction_type = reaction
            old_reaction.save()
    else:
        Like.objects.create(post=post, user=user, ip_address=ip, reaction_type=reaction)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread = notifications.filter(is_read=False)
    unread.update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def delete_notification(request, pk):
    notification = Notification.objects.filter(pk=pk, recipient=request.user).first()
    if notification:
        notification.delete()

    return redirect('notifications')


@login_required
def clear_all_notifications(request):
    Notification.objects.filter(recipient=request.user).delete()
    return redirect('notifications')


def author_leaderboard(request):
    top_authors = User.objects.annotate(
        total_likes=Count('author_posts__likes'),
        post_count=Count('author_posts', distinct=True)
    ).order_by('-total_likes')[:10]

    return render(request, 'leaderboard.html', {'authors': top_authors})



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        message_text = request.POST.get('message')
        if name and message_text:
            ContactMessage.objects.create(name=name, message=message_text)
            send_telegram_message_task.delay(name, message_text)
            messages.success(request, "Xabaringiz yuborildi!")
            return redirect('contact')
    return render(request, 'pages/contact.html')


def terms(request):
    return render(request, 'pages/terms.html')


def privacy(request):
    return render(request, 'pages/privacy.html')



def search_view(request):
    query = request.GET.get('q') 
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |  # Sarlavhadan qidirish
            Q(content__icontains=query) |  # Mazmunidan qidirish
            Q(author__username__icontains=query)  # Muallif ismidan qidirish
        ).distinct()

    return render(request, 'search_results.html', {'query': query, 'results': results})