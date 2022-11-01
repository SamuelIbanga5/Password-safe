from django.urls import path
from .views import (
    registerPage, 
    loginPage, 
    homePage, 
    logoutView, 
    updatePassword, 
    changeAdminPassword, 
    profilePage, 
    editProfile, 
    passwordSafeView,
    getPassword,
    deletePassword,
    )

urlpatterns = [
    path('', homePage, name='home'),
    path('update-password/', updatePassword, name='update-password'),
    path('change-admin-password/', changeAdminPassword, name='change-admin-password'),
    path('get-password/<int:pk>/', getPassword, name='get-password'),
    path('delete-password/<int:pk>/', deletePassword, name='delete-password'),
    path('profile/', profilePage, name='profile'),
    path('edit-profile/', editProfile, name='edit-profile'),
    path('add-password/', passwordSafeView, name='add-password'),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutView, name='logout'),
]