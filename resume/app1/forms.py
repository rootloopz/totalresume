from dataclasses import field
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from .models import Resume


class resumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = "__all__"


#this is the form for creating a new resume
# class CreateMasterResume(forms.Form):
#     #education information
#     Syear = forms.DateField(label="start year")#start year
#     Eyear =  forms.DateField(label="enter your expected graduation year")#end year
#     school = forms.CharField(label="School name:")
#     gpa = forms.FloatField()
#     academAchieve = forms.CharField(label="enter your achievements", widget=forms.Textarea)

#     #job information
#     jobSyear = forms.DateField(label="start year")
#     jobEyear =  forms.DateField(label="enter your end year or none if it is your current job")
#     employerName = forms.CharField(label="Name of your employer")
#     location = forms.CharField(label="location of employer")

#     #skills section
#     skills = forms.CharField(label="skills")

#     #awards / extracariculars
#     awards = forms.CharField(label= "awards")
#     extraCariculars = forms.CharField(label= "enter any extracariculars")

#     #project section
#     projectName = forms.CharField(label="project name")
#     projectDesc = forms.CharField(label="description")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
            'username': None
        } 