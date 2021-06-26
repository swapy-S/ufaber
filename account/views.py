from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProjectDetails
from django.views import View


def index(request):
    return render(request, "account/index.html")


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def projects(request):

    if request.method == "POST":
        task = request.POST["taskname"]
        project = request.POST["project"]
        start = request.POST["start"]
        end = request.POST["end"]
        projectDetails = ProjectDetails(username= request.user.username, taskName = task, projectName = project, start = start, end = end)
        projectDetails.save()
    entries = ProjectDetails.objects.all()
    print(entries)
    li = []
    for i in range(0,len(entries)):
        dic = {}
        dic['task'] = entries[i].taskName
        dic['project'] = entries[i].projectName
        dic['start'] = entries[i].start
        dic['end'] = entries[i].end
        li.append(dic)
    print(li)
    return render(request,'account/projects.html',{'li': li})

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileInfoForm(data=request.POST)
        print("user_form here",user_form)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request,"Account created, click on login!")
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(
        request,
        "account/registration.html",
        {
            "user_form": user_form,
            "registered": registered,
        },
    )

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                entries = ProjectDetails.objects.all()
                print(entries)
                li = []
                for i in range(0,len(entries)):
                    dic = {}
                    dic['task'] = entries[i].taskName
                    dic['project'] = entries[i].projectName
                    dic['start'] = entries[i].start
                    dic['end'] = entries[i].end
                    li.append(dic)
                print(li)
                return render(request,'account/projects.html',{"li":li})
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return render(request, "account/login.html", {'errors':"Invalid login credentials"})
    else:
        return render(request, "account/login.html")
