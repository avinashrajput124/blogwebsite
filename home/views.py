from django.contrib.auth.models import User 
from django.shortcuts import render, redirect, HttpResponse 
from blog.models import Post 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.core.paginator import Paginator, Page

# Create your views here.


def home(request):
    popPost = Post.objects.all()
    items_per_page = 5
    paginator = Paginator(popPost, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'popPost': popPost,'popPost': page,}
    return render(request, 'home/home.html', context)


def search(request):
    query = request.GET['query']
    if len(query) > 80 or len(query) == 0:
        allPost = Post.objects.none()
    else:
        allPosttitle = Post.objects.filter(title__icontains=query)
        allPostauthor = Post.objects.filter(author__icontains=query)
        allPostcontent = Post.objects.filter(content__icontains=query)
        allPost = allPostauthor.union(allPosttitle, allPostcontent)
    if allPost.count() == 0:
        messages.warning(request, 'Please check your query and search again!')
    searchcount = allPost.count()
    context = {'allPost': allPost, 'query': query, 'searchcount': searchcount}
    return render(request, 'home/search.html', context)


def handleSignUp(request):
    if request.method == "POST":
        username = request.POST['signupusername']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if len(username) < 6:
            messages.error(
            request, "Your username must be under 6 characters!")
            return redirect("/")
        
        if not username.isalnum():
            messages.error(
            request, "Your username should only contains letters and numbers!")
            return redirect("/")
        
        if (pass1 != pass2):
            messages.error(
            request, "Your password did not matched!")
            return redirect("/")

        newuser = User.objects.create_user(username, email, pass1)
        newuser.first_name = fname
        newuser.last_name = lname
        newuser.save()
        messages.success(
            request, "Your My Blog account has been successfully created.")
        return redirect("/")

    else:
        return HttpResponse("404-not found")

def handlelogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(
            request, "Successfully logged In.")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials, Please try again!")
            return redirect("/")
    else:
        return HttpResponse("404-Not Found!")

def handlelogout(request):
    user = request.user.is_authenticated
    if user == True:
        logout(request)
        messages.success(request, "User Successfully logged Out")
        return redirect("/")
    else:
        return HttpResponse("404-Not Found!")
    

