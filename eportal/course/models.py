from django.db import models
from user.models import CustomUser
from django_quill.fields import QuillField
from django.core.exceptions import ValidationError



def validate_capitalize(value:str):
    if value[0].islower():
        raise ValidationError(
            ('The field has to start with upper case.')
        )



class Course(models.Model):
    TAG_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(unique=True, max_length=70, validators=[validate_capitalize])              
    description = models.TextField(null=True, blank=True)                                              
    tag = models.CharField(max_length=12, choices=TAG_CHOICES, default="beginner")
    created = models.DateTimeField(auto_now_add=True)
    isPublic = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=70, validators=[validate_capitalize])              
    description = models.TextField(null=True, blank=True)                                   

    def __str__(self):
        return str(self.title)



class Article(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=70, validators=[validate_capitalize])        
    content = QuillField()

    def __str__(self):
        return str(self.title)



class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=70, validators=[validate_capitalize])      

    def __str__(self):
        return str(self.title)



class Results(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.quiz + " " + self.user + " " + self.score)



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, blank=True, null=True, validators=[validate_capitalize])             # walidacja

    def __str__(self):
        return self.question_text



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=255, blank=True, null=True)                
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text