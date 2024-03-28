from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import TechSecurityItem, SecurityFeature, Comment

@admin.register(SecurityFeature)
class SecurityFeatureAdmin(SummernoteModelAdmin):
    """Allows admin to manage security features via the admin panel"""
    list_filter = ('status', 'created_on')
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ('title', 'description')
    summernote_fields = ('description', 'method')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Allows admin to manage comments on security features via the admin panel"""
    list_display = ('name', 'email', 'security_feature', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')

@admin.register(TechSecurityItem)
class TechSecurityAdmin(admin.ModelAdmin):
    """Allows admin to manage tech security items via the admin panel"""
    list_display = ('user', 'day', 'security_feature')
