from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('browsesecurityfeature/', views.SecurityFeatureList.as_view(), name='browse_securityfeatures'),
    path('mysecurityfeatures/', views.MySecurityFeatures.as_view(), name='my_securityfeatures'),
    path('addsecurityfeature/', views.AddSecurityFeature.as_view(), name='add_securityfeature'),
    path('mytechsecurity/', views.TechSecurity.as_view(), name='my_techsecurity'),
    path('bookmark/<slug:slug>/', views.BookmarkSecurityFeature.as_view(), name='bookmark_securityfeature'),
    path('mybookmarks/', views.MyBookmarks.as_view(), name='my_bookmarks'),
    path('securityfeatures/<slug:slug>/', views.SecurityFeatureDetail.as_view(), name='securityfeature_detail'),
    path('securityfeatures/<slug:slug>/update/', views.UpdateSecurityFeature.as_view(), name='update_securityfeature'),
    path('securityfeatures/<slug:slug>/delete/', views.DeleteSecurityFeature.as_view(), name='delete_securityfeature'),
    path('comments/<int:pk>/update/', views.UpdateComment.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    path('like/<slug:slug>/', views.SecurityFeatureLike.as_view(), name='securityfeature_like'),
    path('mytechsecurity/', views.TechSecurity.as_view(), name='my_techsecurity'),
]
