from django.db import models


class Feedback(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]  # Display the first 50 characters in the admin panel