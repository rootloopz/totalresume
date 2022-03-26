from unicodedata import name
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app1.forms import JoinForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

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

# Create your views here.
@login_required
def NewResume(request):
    if request.method == "POST":
        form = CreateMasterResume(request.POST)
    return render(request, "app1/NewResumeForm.html",{
        "form": CreateMasterResume()
    })

def homepage(request):
    return render(request, "app1/welcome.html")

def join(request):
    if(request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            user = join_form.save()
            user.set_password(user.password)
            user.save()
            return redirect("/login/")
        else:
            page_data = { "join_form": join_form }
            return render(request, 'app1/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'app1/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'app1/login.html', {"login_form": LoginForm})
    else:
        #Nothing has been provided for username or password.
        return render(request, 'app1/login.html', {"login_form": LoginForm})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect("/")

###Randall's Stuff###
def GetPDF(request):
    #create byte stream buffer
    buf = io.BytesIO()
    #Create canvas
    c = canvas.Canvas(buf, pagesize=letter,bottomup=0)
    #Create text object
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica", 14)
    #Add lines of text
    lines = ["This is line 1","This is line 2","This is line 3",]
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='something.pdf')