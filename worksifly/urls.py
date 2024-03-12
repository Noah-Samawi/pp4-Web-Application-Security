from . import views
from django.urls import path

urlpatterns = [
    path('', views.SecurityFeatureList.as_view(), name='home'),
    path('<slug:slug>/', views.SecurityFeatureDetail.as_view(), name='securityfeature_detail'),
]
