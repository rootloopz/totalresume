from cProfile import label
from tkinter import Label
from unicodedata import name
from django.shortcuts import render
from django import forms

#this is the form for creating a new resume
class CreateMasterResume(forms.Form):
    #education information
    Syear = forms.DateField(label="start year")#start year
    Eyear =  forms.DateField(label="enter your expected graduation year")#end year
    school = forms.CharField(label="School name:")
    gpa = forms.FloatField()
    academAchieve = forms.CharField(label="enter your achievements", widget=forms.Textarea)

    #job information
    jobSyear = forms.DateField(label="start year")
    jobEyear =  forms.DateField(label="enter your end year or none if it is your current job")
    employerName = forms.CharField(label="Name of your employer")
    location = forms.CharField(label="location of employer")

    #skills section
    skills = forms.CharField(label="skills")

    #awards / extracariculars
    awards = forms.CharField(label= "awards")
    extraCariculars = forms.CharField(label= "enter any extracariculars")

    #project section
    projectName = forms.CharField(label="project name")
    projectDesc = forms.CharField(label="description")




#this is the basic form for getting a username and password from a new user
class NewUser(forms.Form):
    username = forms.CharField(label="desired user name",)
    password = forms.PasswordInput()
    confirmPassword = forms.PasswordInput()



# Create your views here.
def NewResume(request):
    if request.method == "POST":
        form = CreateMasterResume(request.POST)
    return render(request, "app1/NewResumeForm.html",{
        "form": CreateMasterResume()
    })

def GetNewUser(request):
    #if request.method == "POST":
        #form = (request.POST)
    return render(request, "app1/NewUserForm.html",{
        "form": NewUser()
    })

def homepage(request):
    return render(request, "app1/welcome.html")