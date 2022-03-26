from unicodedata import name
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app1.forms import JoinForm, LoginForm, resumeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from app1.models import Resume


# Create your views here.
@login_required
def NewResume(request):
    context = {}
    form = resumeForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()

    context['form'] = form
    return render(request, 'app1/test.html', context)

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
class Sub:
    def __init__(self,title,titleSize,date,dateSize,desc,descSize):
        self.title = title
        self.titleSize = titleSize
        self.date = date
        self.dateSize = dateSize
        self.desc = desc
        self.descSize = descSize

class Subject:
    def __init__(self,title,entries):
        self.title = title
        self.entries = entries

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
    user1 = Resume.objects.get(user = request.user)
    print(f"user =  {user1}")
    fileName = 'SomePDFName.pdf'
    resumeName = 'Randall Fowler'
    contactInfo = '(530)420-6969'
    #subject object
    subject = user1.school
    print(subject)
    date = ['Fall 2019 - Spring 2022']
    description = ['Bachelors of Science, Computer Science - California State University, Chico\nGraduation expected in Spring 2023\nChico GPA: 3.66\nDean\'s list Spring 2021, Fall 2021']
    #description = "\n".join(wrap(description, 500))
    placement = [[40,120]]
    subjDividerY = [200]

    # Education Subject Entries
    EdSub1 = Sub(subject,14,user1.startYear,10,user1.academAchieve,12)
    #Education = Subject("Education",[EdSub1,EdSub1])
    ExSub1 = Sub(user1.employerName,14,user1.employerName,10,user1.academAchieve,12)
    SkSub1 = Sub(user1.skills,14,user1.startYear,10,user1.academAchieve,12)
    ASub1 = Sub(user1.extraCariculars,14,user1.startYear,10,user1.academAchieve,12)
    PSub1 = Sub(user1.projectName,14,user1.startYear,10,user1.academAchieve,12)
    
    Education = Subject("Education",[EdSub1])
    Expierence = Subject("Expierence",[ExSub1])
    Skills = Subject("Skills",[SkSub1])
    Awards = Subject("Awards",[ASub1])
    Projects = Subject("Projects",[PSub1])
    subjects = [Education, Expierence,Skills,Awards,Projects]

    #create byte stream buffer
    buf = io.BytesIO()
    #Create canvas
    pdf = canvas.Canvas(buf, pagesize=letter,bottomup=0)

    # 1) Draw Grid
    #drawRuler(pdf)  #used for creating templates
    
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
    i = 0
    subjectTitleX = 200 #constant
    subjectTitleY = 120
    subTitleX = 40 #constant
    subTitleY = subjectTitleY + 30
    dateX = 440 #constant
    #dateY should be same as subTitleY
    descX = 40  #constant
    descY = subTitleY + 30
    subjectText = pdf.beginText()
    for subject in subjects:
        #Grab Subject: print title
        subjectText.setFont("Helvetica",20)
        subjectText.setTextOrigin(subjectTitleX,subjectTitleY)
        subjectText.textLines(subject.title)
        for sub in subject.entries:
            #grab subject: print title, date, description
            #print title
            subjectText.setFont("Helvetica",sub.titleSize)
            subjectText.setTextOrigin(subTitleX,subTitleY)
            subjectText.textLines(sub.title)
            #print date
            subjectText.setFont("Helvetica",sub.dateSize)
            subjectText.setTextOrigin(dateX,subTitleY)
            subjectText.textLines(sub.date)
            #print description
            subjectText.setFont("Helvetica",sub.descSize)
            subjectText.setTextOrigin(descX,descY)
            subjectText.textLines(sub.desc)
            #change iter for entry
            subTitleY = subTitleY + 90
            descY = subTitleY + 10
        subjectTitleY = subjectTitleY + len(subject.entries)*100
        descY = subTitleY + 30
        #pdf.line(20,subjectTitleY-25,592,subjectTitleY-25)
        pdf.drawText(subjectText)

    pdf.setTitle(resumeName+'Resume')
    pdf.showPage()
    pdf.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=fileName)