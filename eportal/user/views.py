from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, EditUserForm
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
from course.models import Course
from eportal.decorators import (
    redirect_authenticated,
    login_required,
    student_required,
    teacher_required,
)



@redirect_authenticated
def welcome_page(request):
    return render(request, "welcome_page.html")


@student_required
def student_dashboard(request):
    context = {}
    # Filter all courses, where the user is not enrolled
    courses = Course.objects.exclude(
        id__in=request.user.courses.values_list("id", flat=True)
    )

    # Filter public courses
    courses = courses.filter(isPublic=True).order_by('-created') 
    context["courses"] = courses

    return render(request, "user/student_dashboard.html", context)


@teacher_required
def teacher_dashboard(request):
    context = {}
    courses = Course.objects.all()

    # Filter courses both by isPublic and by not author
    courses = courses.filter(isPublic=True).exclude(author=request.user).order_by('-created') 
    context["courses"] = courses

    return render(request, "user/teacher_dashboard.html", context)


# Register view
@redirect_authenticated
def register(request):
    context = {} 

    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.save()
            print("Udało się zapisać nowego Usera") 
            login(request, user)
            if user.role == "student":
                return redirect("student_dashboard")
            else:
                return redirect("teacher_dashboard")
        else:
            print("Nie udało się zapisać nowego Usera")

    context["form"] = form          
    context["disable_navbar"] = True  
    return render(request, "user/register.html", context)


# Login view
@redirect_authenticated
def log_in(request):
    context = {} 

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == "student":            
                return redirect("student_dashboard")
            else:
                return redirect("teacher_dashboard")
        else:
            print("Username albo hasło jest niepoprawne") 

    context["disable_navbar"] = True
    return render(request, "user/login.html", context)


# Logout view
@login_required
def log_out(request):
    logout(request)
    print("Zostałeś wylogowany")

    return redirect('welcome_page')


# Update user view
@login_required
def edit_user(request):
    context = {}

    user = request.user
    form = EditUserForm(instance=user)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("welcome_page")

    context["form"] = form
    return render(request, "user/edit_user.html", context)