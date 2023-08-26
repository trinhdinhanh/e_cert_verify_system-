from random import choices
from sys import maxsize
from django.db import models
from account.models import User




class WaitBlock(models.Model): 
    student_id = models.CharField(max_length=4, null=False, blank=False)
    student_name = models.CharField(max_length=100, null=False, blank=False, default="--")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    course_name = models.CharField(max_length=255, null=False, blank=False)
    final_mark = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return str(self.id)