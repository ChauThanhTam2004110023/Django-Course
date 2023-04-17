from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage.as_view(), name='login'),
    path('logout/', views.logoutPage.as_view(), name='logout'),
    path('register/', views.registerPage.as_view(), name='register'),
    path('', views.home.as_view(), name='home'),
    path('room/<str:pk>/', views.room.as_view(), name='room'),
    path('create-room/', views.createRoom.as_view(), name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom.as_view(), name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom.as_view(), name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage.as_view(), name='delete-message'),
    path('profile/<str:pk>/', views.userProfile.as_view(), name='user-profile')

]