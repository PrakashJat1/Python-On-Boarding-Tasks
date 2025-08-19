from django.db import models


class User(models.Model):

    def __int__(self, name, age, phone_no):
        self.name = name
        self.age = age
        self.phone_no = phone_no

    name = models.CharField(max_length=50)
    age = models.SmallIntegerField()
    phone_no = models.CharField(max_length=10)

    def __str__(self):
        return self.name
