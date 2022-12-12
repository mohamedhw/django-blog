from django.http.request import RAISE_ERROR
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import  login_required
from django.http import JsonResponse




def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request, user)
            
            return redirect("post:list")
    else:
        form = UserForm()
    context = {
        "form": form
    }   
    return render(request, 'user/register.html', context)


@login_required
def profile(request):
    data = {}
    # if request.is_ajax():
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
                # return JsonResponse(data)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,   
        'p_form': p_form
    }
    
    return render(request, 'user/profile.html', context)
