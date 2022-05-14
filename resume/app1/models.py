from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    #contact info, name and more
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=12)
    email = models.EmailField()
    
    objective = models.TextField(blank=True)
    #education information
    startYear = models.CharField(max_length = 4)#start year
    endYear =  models.CharField(max_length = 4, blank=True)#end year
    school = models.CharField(max_length = 100)
    degree = models.CharField(max_length=40)
    degreeType = models.CharField(max_length=50, blank=True)
    gpa = models.CharField(max_length = 4, blank=True)
    schoolextra = models.CharField(max_length = 300, blank=True)

    #job information
    jobStartYear = models.CharField(max_length = 10)
    jobTitle = models.CharField(max_length=40)
    jobEndYear =  models.CharField(max_length = 10, blank=True)
    employer = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100, blank=True)

    #skills section
    skills = models.CharField(max_length = 500, blank=True)

    #awards / extracariculars
    awards = models.CharField(max_length = 500, blank=True)
    extraC = models.CharField(max_length = 1000, blank=True)

    #project section
    projectName = models.CharField(max_length = 100, blank=True)
    projectDesc = models.CharField(max_length = 1000, blank=True)
