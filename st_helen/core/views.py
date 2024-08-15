from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile #imports Profile from the current directory
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login") #redirects to login page if someone tries to access the home page
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
    if request.method == "POST": #POST methods send data from the client to the server 
            username = request.POST["username"] #passing in the argument entered from the form
            password = request.POST["password"]

            user_login = auth.authenticate(username=username, password=password)
            
            if user_login is not None: #checks if the user login exists
                auth.login(request, user_login)
                return redirect("/")
            else:
                messages.info(request, "Invalid credentials") #user doesn't exist message 
                return redirect("signup")

    else:
        return render(request, 'login.html')

@login_required(login_url="login") #only accessible if you're logged in
def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')

def settings(request):
    try:
        user_profile = Profile.objects.get(user=request.user) #getting the information for the currently logged in user
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        if request.FILES.get("image") == None: #checking if user uploaded an image to see if we use the default or theirs
            bio = request.POST["bio"]
            location = request.POST["location"]
            image = user_profile.profileimg

            user_profile.profileimg = image #updating the profile models with the required values 
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get("image") != None:
            bio = request.POST["bio"]
            location = request.POST["location"]
            image = request.FILES.get("image")

            user_profile.profileimg = image #updating the profile models with the required values 
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect ("settings")

    return render(request, "settings.html", {"user_profile": user_profile}) #passing user profile as an object to the html (frontend)
