from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import CustomizeUser, PasswordSafe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, AdminPasswordChangeForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import hashers
from cryptography.fernet import Fernet
from django.conf import settings

f = Fernet(settings.KEY)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreateForm()

        if request.method == 'POST':
            form = UserCreateForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                user = form.cleaned_data['username']
                email = form.cleaned_data['email']
                if CustomizeUser.objects.filter(email=form.cleaned_data['email']).exists():
                    messages.error(request, 'That email already exists!')
                    return HttpResponseRedirect(reverse('register'))
                else:
                    messages.success(request, f'Account has been successfully created for {user}.')
                    return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        # form = AuthenticationForm(request)
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, 'User does not exist')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged is as {request.user}')
                return redirect('home')
            else:
                messages.error(request, 'Account does not exist.')
        else:
            form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)

def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def homePage(request):
    password = PasswordSafe.objects.all().filter(user=request.user)
    context = {'password': password}
    return render(request, 'home.html', context)

@login_required(login_url='login')
def updatePassword(request):
    if request.user.is_superuser:
        return HttpResponseForbidden('<h1>Admins are not allowed to change passwords here!</h1>')
    else:   
        form = PasswordChangeForm(request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed successfully')
                return redirect('home')
            else:
                form = PasswordChangeForm(request.user)
        else:
            form = PasswordChangeForm(user=request.user)
    context = {'form': form}

    return render(request, 'password_Change.html', context)

@login_required(login_url='login')
def changeAdminPassword(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('<h1>Only Admins are allowed to change passwords here!</h1>')
    else:   
        form = AdminPasswordChangeForm(request.user)
        if request.method == 'POST':
            form = AdminPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed successfully')
                return redirect('home')
        else:
            form = AdminPasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'admin_password_change.html', context)

def profilePage(request):

    return render(request, 'profile.html')

def editProfile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return render(request, 'profile.html', {"img_obj": form.instance})
    else:
        form = UserUpdateForm(instance=request.user)

    img_obj = form.instance
    context = {'form': form, 'img_obj': img_obj}
    return render(request, 'edit_profile.html', context)

def passwordSafeView(request):
    form = PasswordSafeForm()
    if request.method == 'POST':
        form = PasswordSafeForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            password = form.password
            encrypted_password = f.encrypt(password.encode())
            form.user = request.user
            form.password = encrypted_password.decode()
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'add_password.html', context)

def getPassword(request, pk):
    # password = PasswordSafe.objects.get(id=pk)
    # token = password.password
    # decrypted_password = f.decrypt(token)
    # context = {'password': password, 'decrypted_password': decrypted_password}
    return render(request, 'get_password.html')

def deletePassword(request, pk):
    if request.method == 'POST':
        password = PasswordSafe.objects.get(id=pk)
        if 'Yes' in request.POST:            
            password.delete()
            return redirect('home')
    return render(request, 'delete_password.html')
