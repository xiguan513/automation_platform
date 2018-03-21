from django.db import models

# Create your models here.

class Dockerenv(models.Model):
    envname = models.CharField(max_length=100,default="environment name")
    envdescribe = models.TextField(default="environment describe")

    def __str__(self):
        return self.envname

class DockerServer(models.Model):
    ip = models.CharField(max_length=100)
    port = models.IntegerField()
    role = models.CharField(max_length=100)
    dockerenv = models.ForeignKey(Dockerenv,on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

class ReDoc(models.Model):
    dockername = models.CharField(max_length=100)
    projectname = models.CharField(max_length=100)
    projecturl = models.CharField(max_length=200)
    projectpath = models.CharField(max_length=200)
    dockerenv = models.ForeignKey(Dockerenv, on_delete=models.CASCADE)

    def __str__(self):
        return self.projectname



