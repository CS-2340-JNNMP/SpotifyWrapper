from django.db import models


class Feedback(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text[:50]  # Display the first 50 characters in the admin panel

class Member(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
