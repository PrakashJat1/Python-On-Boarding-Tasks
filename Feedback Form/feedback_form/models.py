from django.db import models

# Create your models here.


class Feedback(models.Model):
    username = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, blank=False)
    feedback = models.TextField(blank=False)

    def __str__(self):
        return self.username
