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
def drawRuler(pdf):
    pdf.setLineWidth(1)
    pdf.setStrokeColorRGB(0.54,0.54,0.54)
    for x in range(0,610,100):
        pdf.line(x,0,x,900) #draw vertical lines
        pdf.drawString(x,10, 'x'+str(x))
    for y in range(0,900,100):
        pdf.line(0,y,610,y) #draw horizontal lines
        pdf.drawString(10,y, 'y'+str(y))

def GetPDF(request):
    fileName = 'SomePDFName.pdf'
    resumeName = 'Randall Fowler'
    contactInfo = '(916)856-4946'
    #subject object
    subject = ['Education']
    date = ['Fall 2019 - Spring 2022']
    description = ['Bachelors of Science, Computer Science - California State University, Chico\nGraduation expected in Spring 2023\nChico GPA: 3.66\nDean\'s list Spring 2021, Fall 2021']
    placement = [[40,120]]

    #create byte stream buffer
    buf = io.BytesIO()
    #Create canvas
    pdf = canvas.Canvas(buf, pagesize=letter,bottomup=0)

    # 1) Draw Grid
    drawRuler(pdf)  #used for creating templates
    
    # 2) Top Portion
    titleText = pdf.beginText()
    titleText.setTextOrigin(200,50)
    lines = [resumeName,contactInfo]
    fonts = [20,10]
    for i in range(len(lines)):
        titleText.setFont("Helvetica",fonts[i])
        titleText.textLine(lines[i])
    pdf.drawText(titleText)

    # 3) Divider from top
    pdf.setStrokeColorRGB(0,0,0)
    titleDivideLineY = 90
    pdf.line(0,titleDivideLineY,630,titleDivideLineY)

    # 4) Main content
    for i in range(len(subject)):
        subjectText = pdf.beginText()
        titleOffsetX = 200
        subjectText.setTextOrigin(placement[i][0]+titleOffsetX,placement[i][1])
        subjectText.setFont("Helvetica",20)
        subjectText.textLine(subject[i])

        mainOffsetY = 30
        dateOffsetX = 420
        subjectText.setTextOrigin(placement[i][0]+dateOffsetX,placement[i][1]+mainOffsetY)
        subjectText.setFont("Helvetica",12)
        subjectText.textLine(date[i])

        description
        subjectText.setTextOrigin(placement[i][0],placement[i][1]+mainOffsetY)
        #subjectText.setFont("Helvetica",12)
        subjectText.textLine(description[i])

        pdf.drawText(subjectText)








    #Create text object
    #textob = pdf.beginText()
    #textob.setTextOrigin(inch,inch)
    #textob.setFont("Helvetica", 14)
    #Add lines of text
    #lines = ["This is line 1","This is line 2","This is line 3",]
    #for line in lines:
    #    textob.textLine(line)


    pdf.setTitle(resumeName+'Resume')
    #c.drawText(textob)
    pdf.showPage()
    pdf.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=fileName)