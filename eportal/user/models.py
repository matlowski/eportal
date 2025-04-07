from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Uczeń"),
        ("teacher", "Nauczyciel"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    courses = models.ManyToManyField("course.Course", through="Enrollment", blank=True) 
    


class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return self.user.username + " - " + self.course.title
