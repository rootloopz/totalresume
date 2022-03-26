from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #education information
    startYear = models.CharField(max_length = 4)#start year
    endYear =  models.CharField(max_length = 4)#end year
    school = models.CharField(max_length = 100)
    gpa = models.CharField(max_length = 4)
    academAchieve = models.CharField(max_length = 300)

    #job information
    jobStartYear = models.CharField(max_length = 10)
    jobEndYear =  models.CharField(max_length = 10)
    employerName = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)

    #skills section
    skills = models.CharField(max_length = 500)

    #awards / extracariculars
    awards = models.CharField(max_length = 500)
    extraCariculars = models.CharField(max_length = 1000)

    #project section
    projectName = models.CharField(max_length = 100)
    projectDesc = models.CharField(max_length = 1000)
