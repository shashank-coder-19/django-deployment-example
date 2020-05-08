from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    print('You are logged in, Nice!')

@login_required
def user_logout(request):
    logout(request)
    print('i am logged out')
    return HttpResponseRedirect(reverse('index'))
    # above i have used a decorator
    # i have to use it because i do not want to use logout if i am not login that is why a decorator is being used

def register(request):
    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()
            user.set_password(user.password)
            # it is hashing the  password and saving it to the setting.py file
            user.save()

            profile=profile_form.save(commit=False)
            # i have saved it commit equal to false because i do not want to directly save it to database
            profile.user=user
            # i am establishing here one to one relantionship with the user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
                # request.FILES act as a dictionary and we are looking for 'profile_pic' key
            profile.save()
            registered=True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # this get keyword requires same variable as you have written in name of their specific input in their html file

        user=authenticate(username=username,password=password)
        # we can authenticate user using its built in authenticate function

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')

        else:
            print('someone tried to login and failed')
            print('Username:{} and password:{}'.format(username,password))
            print('invalid login details supplied')

    else:
        return render(request,'basic_app/login.html',{})
