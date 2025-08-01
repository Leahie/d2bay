from django.contrib import admin
from core_social.models import Trade, Profile, Comment, Like, FollowingRelationships

# Register your models here.
admin.site.register(Profile)
admin.site.register(Trade) 
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FollowingRelationships)