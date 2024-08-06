from django.db import models

# Create your models here.

class logintable(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    type=models.CharField(max_length=50)

class securitytable(models.Model):
    LOGIN=models.ForeignKey(logintable,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    idproof=models.FileField()
    phone=models.BigIntegerField()
    email=models.CharField(max_length=50)

class assignworktable(models.Model):
    security=models.ForeignKey(securitytable,on_delete=models.CASCADE)
    work=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)

class complainttable(models.Model):
    security=models.ForeignKey(securitytable,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)
    date=models.DateField()

class feedbacktable(models.Model):
    security = models.ForeignKey(securitytable, on_delete=models.CASCADE)
    comments=models.CharField(max_length=100)
    date=models.DateField()

class reporttable(models.Model):
    assignwork = models.ForeignKey(assignworktable, on_delete=models.CASCADE)
    report=models.CharField(max_length=100)
    date=models.DateField()
    description=models.CharField(max_length=100)

class cameratable(models.Model):
    camera_no=models.IntegerField()
    latitude=models.FloatField()
    longitude=models.FloatField()

class alerttable(models.Model):
    camera=models.ForeignKey(cameratable,on_delete=models.CASCADE)
    alerttype=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    image=models.FileField()

class emotiontable(models.Model):
    camera = models.ForeignKey(cameratable, on_delete=models.CASCADE)
    emotion=models.CharField(max_length=100)
    date=models.DateField()
    image=models.FileField()
