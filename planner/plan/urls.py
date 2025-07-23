from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('plan/<int:pk>/edit/', views.edit_plan, name='edit_plan'),
    path('plan/<int:pk>/delete/', views.delete_plan, name='delete_plan'),
    path('plan/<int:pk>/', views.plan_detail, name='plan_page'),
    path('plan/<int:pk>/', views.plan_page, name='plan_detail'),
    path('create_plan/', views.create_plan, name='create_plan'),
    path('plan/<int:pk>/edit/', views.edit_plan, name='edit_plan'),
    path('categories/<int:pk>/', views.category_page, name='category_detail'),

    # 🔐 Auth routes
    path('register/', views.Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('search/', views.search, name='search'),
]
