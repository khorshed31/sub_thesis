from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import user as myUser

# Create your views here.
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        userName = request.POST['username']
        # userRole = request.POST['role']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=userName).exists():
                messages.error(request, 'Username already exist!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exist!')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=userName, password=password, email=email)
                user.save()

                # user1 = myUser(fullName,userName,'',email,password)
                # user1.save()
                return redirect('signin')
        else:
            messages.error(request, 'Password and confirm password doesnt match')
    return render(request,'account/signup.html')

def signin(request):
    if request.method == 'POST':
        userName=request.POST['username']
        password =request.POST['password']
        user = authenticate(request,username=userName,password=password)
        user.save()
        
        if user is not None:
            login(request,user)
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Invalid Username or Password!')
    else:
        return render(request,'index.html')
def signout(request):
    logout(request)
    messages.success(request, 'Successfully Logout!!.')
    return redirect('signin')
