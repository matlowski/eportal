from django.urls import path
from . import views


urlpatterns = [
    path("add_course/", views.add_course, name="add_course"),
    path("add_lesson/<str:course_pk>/", views.add_lesson, name="add_lesson"),
    path("edit_course/<str:course_pk>/", views.edit_course, name="edit_course"),
    path("delete_course/<str:course_pk>/", views.delete_course, name="delete_course"),
    path("edit_lesson/<str:lesson_pk>/", views.edit_lesson, name="edit_lesson"),
    path(
        "edit_question/<str:lesson_pk>/<str:question_pk>/",
        views.add_or_edit_question,
        name="edit_question",
    ),
    path(
        "edit_question/<str:lesson_pk>/",
        views.add_or_edit_question,
        name="add_question",
    ),
    path(
        "edit_answer/<str:lesson_pk>/<str:question_pk>/<str:answer_pk>/",
        views.add_or_edit_answer,
        name="edit_answer",
    ),
    path(
        "edit_answer/<str:lesson_pk>/<str:question_pk>/",
        views.add_or_edit_answer,
        name="add_answer",
    ),
    path(
        "delete_question/<str:lesson_pk>/<str:question_pk>/",
        views.delete_question,
        name="delete_question",
    ),
    path(
        "delete_answer/<str:lesson_pk>/<str:answer_pk>/",
        views.delete_answer,
        name="delete_answer",
    ),
    path("lesson/delete/<str:pk>/", views.delete_lesson, name="delete_lesson"),
    path(
        "course_detail/<str:course_pk>/",
        views.course_detail,
        name="course_detail",
    ),
    path("author_courses/", views.author_courses, name="author_courses"),
    path("my_courses/", views.my_courses, name="my_courses"),
    path("my_results/", views.my_results, name="my_results"),
    path(
        "start_learning/<str:course_pk>/", views.start_learning, name="start_learning"
    ),
    path("show_lesson/<str:lesson_pk>", views.show_lesson, name="show_lesson"),
    path("show_lessons/<str:course_pk>", views.show_lessons, name="show_lessons"),
    path(
        "show_article/<str:lesson_pk>/<str:course_pk>",
        views.show_article,
        name="show_article",
    ),
    path(
        "show_quiz/<str:lesson_pk>/<str:course_pk>", views.show_quiz, name="show_quiz"
    ),
    path("submit_quiz/<str:quiz_id>", views.submit_quiz, name="submit_quiz"),
]
