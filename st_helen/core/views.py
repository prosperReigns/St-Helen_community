from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile #imports Profile from the current directory

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST": #python checks if it is a post method (validation)
        username = request.POST["username"] #python looks at the form and makes the username 
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2: #checking if passwords are equal (validation)
            if User.objects.filter(email=email).exists(): #checking the email does not already exist in the database (that django created called objects)
                messages.info(request, "Email taken") #gives a message to the user
                return redirect("signup") #reloads the page
            elif User.objects.filter(username=username).exists(): 
                messages.info(request, "Username already taken")
                return redirect("signup")
            elif username == "": #checks if username is empty
                messages.info(request, "Username cannot be empty")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=password) #creates a user in the database
                user.save()
                #log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username) #gets the username of the new user 
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect("login") #edit later 

        else:
            messages.info(request, "Password does not match") #*
            return redirect("signup")

    else:
        return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'logout.html')