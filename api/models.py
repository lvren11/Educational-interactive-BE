from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    school = models.CharField(u'school', max_length=100)
    snumber = models.CharField(u'snumber', max_length=100)
    grade = models.CharField(u'grade', max_length=100)
    classes = models.CharField(u'classes', max_length=100)
    sex = models.CharField(u'sex', max_length=100)
    name = models.CharField(u'name',max_length=100)

class Usertoken(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(to='User', on_delete=models.CASCADE)
    token = models.CharField(max_length=1000)

class UserLog(models.Model):
    id = models.AutoField(primary_key=True)
    snumber = models.CharField(u'snumber', max_length=100)
    logname = models.CharField(max_length=1000)