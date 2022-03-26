from cProfile import label
from unicodedata import name
from django.shortcuts import render
from django import forms

class CreateMasterResume(forms.Form):
    school = forms.TextInput()#label="School name:")
    degree = forms.FloatField()#label="GPA")


# Create your views here.
def NewResume(request):
    if request.method == "POST":
        form = CreateMasterResume(request.POST)
    return render(request, "app1/NewResumeForm.html",{
        "form": CreateMasterResume()
    })