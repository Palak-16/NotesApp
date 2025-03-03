from django.contrib import admin
from django.urls import path
from notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("notes", views.notes, name="notes"),
    path("signup", views.signup, name="signup"),
    path("login", views.user_login, name="user_login"),
    path("logout", views.user_logout, name="user_logout"),
    path("loggedin", views.loggedin, name="loggedin"),
    path("addnote", views.addnote, name="addnote"),
    path('editnote/<int:note_id>/', views.editnote, name="editnote"),
    path('deletenote/<int:note_id>/', views.deletenote, name="deletenote")
    
]
