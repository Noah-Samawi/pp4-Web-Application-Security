from django.contrib import admin
from .models import SecurityFeature, TechSecurityItem, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(SecurityFeature)
class SecurityFeatureAdmin(SummernoteModelAdmin):
    """Allows admin to manage security_feature via the admin panel"""
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Allows admin to manage comments on recipes via the admin panel"""
    list_display = ('get_name', 'body', 'security_feature', 'created_on')  
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def get_name(self, obj):
        return obj.name
    def approve_comments(self, recipes, queryset):
        queryset.update(approved=True)

# @admin.register(TechSecurityItem)
# class TechSecurityItemAdmin(admin.ModelAdmin):
#     """Allows admin to manage user Tech Security  via the admin panel"""
#     list_display = ('user', 'security_feature', 'day')