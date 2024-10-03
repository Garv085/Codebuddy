from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name = "login-page"),
    path('logout/', views.LogoutPage, name = "logout-page"),
    path('register/', views.RegisterPage, name = "register-page"),
    path('', views.home, name = "home" ),
    path('room/<str:pk>', views.room, name = "room"),
    path('UserProfile/<str:pk>', views.UserProfile, name = "user-profile"),
    path('create-room/', views.create_room, name = "create-room"),
    path('update-room/<str:pk>', views.update_room, name = "update-room"),
    path('delete-room/<str:pk>', views.delete_room, name = "delete-room"),
    path('delete-message/<str:pk>', views.delete_message, name = "delete-message"),
    path('new_topic/', views.create_topic, name = 'create-topic')
]