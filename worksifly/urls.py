from . import views
from django.urls import path

urlpatterns = [
    # Home page
    path('', views.Home.as_view(), name='home'),

    # Browse security features page
    path('browsesecurityfeature/', views.SecurityFeatureList.as_view(), name='browse_securityfeatures'),

    # My security features page
    path('mysecurityfeatures/', views.MySecurityFeatures.as_view(), name='my_securityfeatures'),

    # Add security feature page
    path('addsecurityfeature/', views.AddSecurityFeature.as_view(), name='add_securityfeature'),

    # My tech security page
    path('mytechsecurity/', views.TechSecurity.as_view(), name='my_techsecurity'),

    # Bookmark security feature
    path('bookmark/<slug:slug>/', views.BookmarkSecurityFeature.as_view(), name='bookmark_securityfeature'),

    # My bookmarks page
    path('mybookmarks/', views.MyBookmarks.as_view(), name='my_bookmarks'),

    # Security feature detail page
    path('securityfeatures/<slug:slug>/', views.SecurityFeatureDetail.as_view(), name='securityfeature_detail'),

    # Update security feature page
    path('securityfeatures/<slug:slug>/update/', views.UpdateSecurityFeature.as_view(), name='update_securityfeature'),

    # Delete security feature page
    path('securityfeatures/<slug:slug>/delete/', views.DeleteSecurityFeature.as_view(), name='delete_securityfeature'),

    # Update comment page
    path('comments/<int:pk>/update/', views.UpdateComment.as_view(), name='update_comment'),

    # Delete comment page
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),

    # Like/unlike a security feature
    path('like/<slug:slug>/', views.SecurityFeatureLike.as_view(), name='securityfeature_like'),

    # My tech security page (duplicate entry, remove one)
    # path('mytechsecurity/', views.TechSecurity.as_view(), name='my_techsecurity'),
]
