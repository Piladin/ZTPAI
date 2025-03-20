from django.urls import path
from .views import (
    register, 
    login, 
    announcement_list, 
    add_announcement, 
    edit_announcement, 
    edit_user,
    delete_announcement,
    get_current_user,
    get_announcement,
    search_announcements
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('announcements/', announcement_list, name='announcement_list'),
    path('announcements/<int:pk>/', get_announcement, name='get_announcement'),
    path('announcements/add/', add_announcement, name='add_announcement'),
    path('announcements/edit/<int:pk>/', edit_announcement, name='edit_announcement'),
    path('announcements/delete/<int:pk>/', delete_announcement, name='delete_announcement'),
    path('user/edit/', edit_user, name='edit_user'),
    path('user/me/', get_current_user, name='get_current_user'),
    path('announcements/search/', search_announcements, name='search_announcements'),
]