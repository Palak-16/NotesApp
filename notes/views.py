from pyexpat.errors import messages
from django.shortcuts import redirect, render , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login ,authenticate,logout
from django.contrib import messages  # ✅ Correct import
from django.contrib.messages import get_messages
from notes.models import Notes
import bleach

# Create your views here.
def home(request):
    return render(request,'home.html')

def signup(request):
    storage = get_messages(request)  # Clear old messages
    for _ in storage:
        pass
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        # phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
         
         # Auto-login After Registration
        login(request,user)
        messages.success(request, "Account created successfully!")
        return redirect('user_login')  # Change 'home' to the desired redirect page
    return render(request, 'signup.html')

def user_login(request):
    storage = get_messages(request)  # Clear old messages
    for _ in storage:
        pass  # This ensures messages are read and cleared
    if request.method == "POST":
        loginusername = request.POST.get("loginusername")
        loginpassword = request.POST.get("loginpassword")

        user = authenticate(request, username=loginusername, password=loginpassword)
        if user != None :
            login(request,user)
            messages.success(request, "successfully logged in!")
            return redirect('notes')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('user_login')

    return render(request, 'login.html')

# def user_logout(request):
#     return render(request, 'home.html')

def loggedin(request):
    return render(request, 'loggedin.html')

def notes(request):
     # Fetch notes only for the logged-in user
    user_notes = Notes.objects.filter(user=request.user).order_by('-created_at')  # Latest first
    
    context = {'notes': user_notes}

    return render(request, 'notes.html', context)

def addnote(request):
    storage = get_messages(request)  # Clear old messages
    for _ in storage:
        pass
    if request.method == "POST":
        
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            Notes.objects.create(user=request.user, title=title, content=content)
            messages.success(request, "Note saved successfully!") 
            return redirect('notes')  # Change 'home' to the desired redirect page
        else:
            messages.error(request, "Invalid Input")
    return render(request, 'addnote.html')

def editnote(request, note_id):
    storage = get_messages(request)  # Clear old messages
    for _ in storage:
        pass

    # note = get_object_or_404(Notes, id=note_id, user=request.user)
    note = get_object_or_404(Notes, id=note_id)
    if request.method == "POST":
        note.title = request.POST.get("title")
        note.content = request.POST.get("content")
        note.save()
        return redirect('notes')  # Change 'home' to the desired redirect page
    
    return render(request, 'editnote.html', {'note': note})

def deletenote(request, note_id):
    note = get_object_or_404(Notes, id=note_id, user=request.user)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted successfully!")
        return redirect('notes')
    
    return render(request, 'deletenote.html',{'note': note})

