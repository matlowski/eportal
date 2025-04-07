from django import forms
from django_quill.forms import QuillFormField
from .models import Course, Lesson, Article, Quiz, Question, Answer



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "tag", "isPublic"]


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description"]


class ArticleForm(forms.ModelForm):
    content = QuillFormField()

    class Meta:
        model = Article
        fields = ["title", "content"]


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["answer_text", "is_correct"]
