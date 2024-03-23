from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import TechSecurityItem, SecurityFeature, Comment


@admin.register(SecurityFeature)
class SecurityFeatureAdmin(SummernoteModelAdmin):
    """Allows admin to manage security feature via the admin panel"""
    list_filter = ('status', 'created_on')
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ('title', 'description')
    summernote_fields = ('description', 'method')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Allows admin to manage comments on security feature via the admin panel"""
    list_display = ('get_name', 'body', 'security_feature', 'created_on')  
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def get_name(self, obj):
        return obj.name

    def approve_comments(self, securityfeatures, queryset):
        queryset.update(approved=True)


@admin.register(TechSecurityItem)
class TechSecurityAdmin(admin.ModelAdmin):
    """Allows admin to manage user Tech Security  via the admin panel"""
    list_display = ('user', 'security_feature', 'day')
