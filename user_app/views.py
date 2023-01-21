from django.shortcuts import render,redirect

from .forms import *
from django.contrib import messages


def register(request):
    if request.method =='POST':
        form =RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form =RegisterForm()
    return render(request, 'user_app/register.html',{'form':form})

def profile(request):
    return render(request, 'user_app/profile.html')

def profileupdate(request):

    if request.method == 'POST':
        u_form = UpdateRegisterForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, 'successfully updated')
            return redirect('profile')

    else:
        u_form =  UpdateRegisterForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

    context = {

        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'user_app/profileupdate.html', context)