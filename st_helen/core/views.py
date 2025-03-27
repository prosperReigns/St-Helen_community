from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, LikePost, Question, Option, Response, Student, Club #imports LikePost, Posts, Questions, Option and Response from the current directory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout 
from .functions.matching import calculate_match_score

# Create your views here.
@login_required(login_url="login") #redirects to login page if someone tries to access the home page
def index(request):
    post=Post.objects.all().order_by("-created_at")
    return render(request, 'index.html', {"posts":post})

def signup(request):
    if request.method == "POST": #python checks if it is a post method (validation)
        username = request.POST["username"] #python looks at the form and makes the username 
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2: #checking if passwords are equal (validation)
            if not email.endswith("@sthelens.london"):
                messages.info(request, "Must be a St Helen's student to sign up") #checks if user is a student 
                return redirect("signup")

            if User.objects.filter(email=email).exists(): #checking the email does not already exist in the database (that django created called objects)
                messages.info(request, "Email taken") #gives a message to the user
                return redirect("signup") #reloads the page
            elif User.objects.filter(username=username).exists(): 
                messages.info(request, "Username already taken")
                return redirect("signup")
            elif username == "": #checks if username is empty
                messages.info(request, "Username cannot be empty")
                return redirect("signup")
            
            elif len(password) <8: #adding a minimum length of characters for password 
                messages.info(request, "Password must be at least 8 characters long")
                return redirect ("signup")
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password) #creates a user in the database
                user.save()

                Student.objects.create(user=user)

                #log user in as soon as they signup
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username) #gets the username of the new user 
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect("quiz") #redirects the user to the quiz/assessment view

        else:
            messages.info(request, "Password does not match") #*
            return redirect("signup")

    else:
        return render(request, 'signup.html')
    

@login_required
def quiz(request):
    questions = Question.objects.all().order_by("id") # gets all the questions and orders them in ascending order
    student = request.user.student #track who takes the quiz

    if request.method == "POST": #will be sending information to the database
        question_id = request.POST.get("question_id")
        chosen_option = request.POST.get("chosen_option")

        question = Question.objects.get(id=question_id) #getting the corresponding question and option from the database
        chosen_option = Option.objects.get(id=chosen_option)

        Response.objects.update_or_create( #overwrites an existing record or creates a new one
            student = student, 
            question = question,
            defaults = {"option" : chosen_option}
        )

        next_question_id = question.id + 1 #increments the ID 
        next_question = Question.objects.filter(id=next_question_id).first()

        if next_question:
            return render(request, "quiz.html", {"question": next_question}) #if there are more questions
        else:
            return render(request, "quiz_complete.html") #goes to the complete page (will add later)
        
    return render(request, "quiz.html", {"question": Question.objects.first()}) 


def login(request):
    if request.method == "POST": #POST methods send data from the client to the server 
            username = request.POST["username"] #passing in the argument entered from the form
            password = request.POST["password"]

            user_login = auth.authenticate(username=username, password=password)
            
            if user_login is not None: #checks if the user login exists
                auth.login(request, user_login)

                if user_login.is_superuser: #redirect to admin page if admin credentials are accurate
                    return redirect("/admin/")

                return redirect("/")
            else:
                messages.info(request, "Invalid credentials") #user doesn't exist message 
                return redirect("login")

    else:
        return render(request, 'login.html')

@login_required(login_url="login") #only accessible if you're logged in
def logout(request):
    auth.logout(request) #logs the user out 
    return redirect (login) #redirects to the signup page 


@login_required(login_url="login") #only accessible if you're logged in
def settings(request):
    try:
        user_profile = Profile.objects.get(user=request.user) #if the user already has a profile, retrieve this
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user) #if they don't have a profile, create one


    if request.method == "POST":
        image = request.FILES.get("image", user_profile.profileimg)
        bio = request.POST.get("bio", "")
        year_group = request.POST.get("year_group", user_profile.year_group)

        user_profile.profileimg = image #save the uploaded image
        user_profile.bio = bio #save the uploaded bio
        user_profile.year_group = year_group #save the selected year group
        user_profile.save() #update the user profile
        
        return redirect ("settings")

    return render(request, "settings.html", {"user_profile": user_profile, "YEAR_GROUP_CHOICES": Profile.YEAR_GROUP_CHOICES}) #passing user profile to the frontend


@login_required(login_url="login")
def connect(request):
    current_student = request.user.student #retrieves the current user
    current_student_responses = Response.objects.filter(student=current_student) #gets all the user's responses 

    other_responses = Response.objects.exclude(student=current_student) #gets all other responses except the user's

    matches = [] #creates the matches list 
    viewed_students = [] #creates a list for students who have been searched already to prevent duplicates 

    for response in other_responses:
        student_response = current_student_responses.filter(question=response.question).first() #filters responses based on the question 

        if student_response: #if the student has answered 
            score = calculate_match_score(current_student,response.student) #calls the matching algorithm 

            if score>=3 and response.student not in viewed_students: #only show a match if they have a score greater than 3 and they are not in the list already
                matched_student = response.student
                matched_user = matched_student.user #retrieves the user information of the matched student
                matched_profile = Profile.objects.get(user=matched_user) #retrieves that user's profile
                
                if matched_student: #only if matched_student is valid
                    matches.append ({
                        'student':matched_student,
                        'score':score,
                        'username':matched_user.username, #gets their username from user model
                        'email':matched_user.email, #gets their email from user model
                        'bio':matched_profile.bio, #gets their bio from profile model
                        'profileimg':matched_profile.profileimg.url #gets their profileimg from profile model
                    }) #adds the user to the matches list 

                    viewed_students.append(matched_student) #appends the student to the viewed list 


    matches = sorted(matches, key=lambda x:x['score'], reverse=True) #sorts the list in descending order so matches go by highest to lowest 

    return render (request, "connect.html", {'matches':matches})

@login_required(login_url="login")
def discover(request):
    category = request.GET.get('category') #get the parameters necessary for the filter 
    clubs=Club.objects.all().order_by("id") #show all clubs, order them by their id

    if category: #if a category is passed 
        clubs = clubs.filter(club_category=category) #'clubs' variable now becomes all clubs under this category

    return render(request, 'discover.html', {"clubs":clubs}) #render the discover.html page


@login_required(login_url="login")
def makepost(request):
    if request.method == 'POST':
        user = request.user #retrieves the username of the user from the form
        image = request.FILES.get('image_upload') #retrieves the image to be posted from form
        caption = request.POST["caption"] #retrieves the caption from the form

        new_post = Post.objects.create(user=user, image=image, caption=caption) #creates a new post to the post model
        new_post.save() #saves the post to the database

        return redirect("/")
    else:
        return redirect("/")


@login_required(login_url="login")
def likepost(request):
    user=request.user #gets username of logged in user
    post_id=request.GET.get('post_id') #retrieves the post ID 

    post = Post.objects.get(id=post_id)
    like_filter=LikePost.objects.filter(post=post, user=user).first()

    if like_filter == None: #if the user hasn't liked the post yet 
        new_like=LikePost.objects.create(post=post, user=user) #creates a new like
        new_like.save() 
        post.no_of_likes=post.no_of_likes+1 #increments the number of likes by 1
        post.save()
        return redirect('/')
    else: #if the user has already liked the post before 
        like_filter.delete() #removes the like
        post.no_of_likes=post.no_of_likes-1 #removes the like
        post.save()
        return redirect('/')

@login_required(login_url="login")
def profileview(request, username): #takes in the username of the user who's profile you want to see
    user_object = User.objects.get(username=username) #creates an object of that user 
    user_profile = Profile.objects.get(user=user_object) #gets that user's profile
    user_posts = Post.objects.filter(user=user_object).order_by("-created_at") #get all the posts posted by that user 

    context = {
        "user_object": user_object,
        "user_profile": user_profile,
        "user_posts": user_posts,
    } #passes this code to the frontend for reference sake 
    return render(request,'profile.html', context) 
