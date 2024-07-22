from django.db import models
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    price = models.IntegerField()
    grade = models.IntegerField()
    add_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.add_date + relativedelta(months=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
