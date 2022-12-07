from django.shortcuts import render,redirect
from .models import Profile,Dweet
from .forms import DweetForm,CustomUserCreationForm
from django.contrib.auth import login
from django.urls import reverse

def dashboard(request):
    if request.user.is_authenticated :
        
        form = DweetForm(request.POST or None)
        if request.method == "POST":
            # form = DweetForm(request.POST)#fill the form to the new data 
            if form.is_valid():
                dweet = form.save(commit=False)
                dweet.user = request.user#get the user who added the dweet
                dweet.save()
                return redirect("dwitter:dashboard")#GET
        followed_dweets = Dweet.objects.filter(
            user__profile__in=request.user.profile.follows.all()).order_by("-created_at")
        return render(request, "dwitter/dashboard.html", {"form": form,"dweets":followed_dweets})
    
    else:
        return redirect("dwitter:login")
        

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request,"dwitter/profile_list.html",{"profiles": profiles})

def profile(request,pk):
    #if the user has no profile
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
        
    profile=Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST#get the data from the request
        action = data.get("follow")#get the value of the attribute named follow
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request,"dwitter/profile.html",{"profile":profile})

def register(request):
    if request.method == "GET":
        return render(
            request, "dwitter/register.html",
            {"form": CustomUserCreationForm})
        
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect(reverse("dwitter:dashboard"))