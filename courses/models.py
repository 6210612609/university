from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=64)
    maxquantity = models.IntegerField()
    nowquantity = models.IntegerField(default=0)
    semester = models.IntegerField(default=None)
    year = models.IntegerField(default=None)
    students = models.ManyToManyField(User, blank=True, related_name="courses")
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} : {self.name}"