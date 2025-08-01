from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

"""Profile model for extending user information in a social media application."""
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    interest_field = [
            ('music', 'Music'),
            ('sports', 'Sports'),
            ('travel', 'Travel'),
            ('reading', 'Reading'),
            ('gaming', 'Gaming'),
        ]
    
    interests = models.CharField(
        choices=interest_field,
        max_length=20,
        null=True,
        blank=True
    )
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"
    
class FollowingRelationships(models.Model):
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='following'# profile.following.all = who is the user following
    )
    following = models.ForeignKey( # profile.followers.all = who is following the user 
        Profile, on_delete=models.CASCADE, related_name='followers' # many-to-many relationship
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"

class Trade(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='trades')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='trade_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.trade.id} at {self.created_at}"

class Like(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trade', 'profile')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile.user.username} liked trade {self.trade.id} at {self.created_at}"

# Signals to create and save the profile automatically when a user is created or updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()