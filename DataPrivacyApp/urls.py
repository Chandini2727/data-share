from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
			path("Login.html", views.Login, name="Login"),
			path("LoginAction", views.LoginAction, name="LoginAction"),
			path("Signup.html", views.Signup, name="Signup"),
			path("SignupAction", views.SignupAction, name="SignupAction"),	    
			path("PostMessage.html", views.PostMessage, name="PostMessage"),
			path("PostMessageAction", views.PostMessageAction, name="PostMessageAction"),	  
			path("ViewMessage", views.ViewMessage, name="ViewMessage"),
]