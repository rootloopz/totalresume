from cProfile import label
from unicodedata import name
from django.shortcuts import render
from django import forms

class CreateMasterResume(forms.Form):
    school = forms.CharField(label="School name:")#label="School name:")
    gpa = forms.FloatField()#label="GPA")

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