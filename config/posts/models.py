from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    keywords = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"{self.post.title} rasmi"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} profili"

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    viewer_ip = models.CharField(max_length=45)
    viewed_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    REACTION_CHOICES = [
        ('like', '❤️ Like'),
        ('haha', '😂 Haha'),
        ('wow', '😮 Wow'),
        ('sad', '😢 Sad'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES, default='like')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProfileComment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} -> {self.profile.user.username}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Izoh'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} dan xabar"


# --- Signals ---

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.user:
        if instance.post.author != instance.user:
            Notification.objects.create(
                recipient=instance.post.author,
                sender=instance.user,
                notification_type='like',
                post=instance.post
            )