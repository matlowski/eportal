from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Lesson, Article, Quiz, Question, Answer, Results
from eportal.decorators import login_required, student_required, teacher_required
from .forms import CourseForm, LessonForm, ArticleForm, QuizForm, QuestionForm, AnswerForm
from user.models import Enrollment
from django.core.exceptions import PermissionDenied



# Display details of a selected course
@login_required 
def course_detail(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    lessons = course.lesson_set.all()
    for lesson in lessons:
        try:
            lesson.article = lesson.article
        except:
            lesson.article = None
        try:
            lesson.quiz = lesson.quiz
        except:
            lesson.quiz = None
    context = {"course": course, "lessons": lessons}
    return render(request, "course/course_detail.html", context)


# Display all courses created by the teacher
@teacher_required 
def author_courses(request):
    user = request.user 
    courses = Course.objects.filter(enrollment__user=user).order_by("-enrollment__date_enrolled") 
    context = {"courses": courses}
    return render(request, "user/teacher_dashboard.html", context)


# Display all courses – homepage 
@login_required 
def my_courses(request):
    user = request.user 
    if user.role == "teacher": 
        return redirect("author_courses")
    
    courses = user.courses.filter(isPublic=True) 
    courses = courses.filter(enrollment__user=user).order_by("-enrollment__date_enrolled")  
    context = {"courses": courses}
    return render(request, "user/my_courses.html", context)


# Enrolling in a course by a student
@student_required
def start_learning(request, course_pk):
    user = request.user 
    course = Course.objects.get(pk=course_pk) 
    user.courses.add(course) 
    return redirect("show_lessons", course_pk=course_pk) 


# Displaying all lessons within a course
@student_required 
def show_lessons(request, course_pk): 
    course = get_object_or_404(Course, pk=course_pk)  
    if not Enrollment.objects.filter(user=request.user, course=course).exists(): 
        raise PermissionDenied                                              
    lessons = course.lesson_set.all()
    context = {"course": course, "lessons": lessons}
    return render(request, "course/show_lessons.html", context)


# Displaying a single lesson within a course
@login_required 
def show_lesson(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk) 
    course = lesson.course 
    if not Enrollment.objects.filter(user=request.user, course=course).exists(): 
        raise PermissionDenied                                         
    lesson = Lesson.objects.select_related("article", "quiz").get(pk=lesson_pk, course=course)
    context = {
        "lesson": lesson,
        "article": getattr(lesson, "article", None),  
        "quiz": getattr(lesson, "quiz", None),  
    } 
    return render(request, "course/show_lesson.html", context)


# Displaying an article within a specific lesson in the course by a student or teacher
@login_required 
def show_article(request, lesson_pk, course_pk):
    course = Course.objects.get(pk=course_pk) 
    lesson = course.lesson_set.get(pk=lesson_pk)
    article = lesson.article 
    context = {"article": article}
    return render(request, "course/show_article.html", context)


# Displaying a quiz (for reading) within a specific lesson in the course by the teacher
@teacher_required 
def show_quiz(request, lesson_pk, course_pk):    
    course = Course.objects.get(pk=course_pk)  
    lesson = course.lesson_set.get(pk=lesson_pk) 
    quiz = lesson.quiz 
    questions = quiz.question_set.all() 
    for question in questions: 
        question.answers.all() 
    context = {"quiz": quiz, "questions": questions}
    return render(request, "course/show_quiz.html", context)


# Displaying the quiz results of a specific student
@student_required 
def my_results(request):
    student = request.user 
    results = student.results_set.all() 
    for result in results: 
        result.quiz.lesson.course 
    results = results.order_by("-created")   
    context = {"results": results}
    return render(request, "course/my_results.html", context)


# Editing the course by the teacher who is a participant (and author) of it
@teacher_required 
def edit_course(request, course_pk):
    user = request.user 
    try:
        course = user.course_set.get(pk=course_pk) 
    except Course.DoesNotExist: 
        return redirect("teacher_dashboard")
    if request.method == "POST": 
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("author_courses")  
    else: 
        form = CourseForm(instance=course)

    lessons = course.lesson_set.all() 
    context = {"form": form, "course": course, "lessons": lessons} 
    return render(request, "course/edit_course.html", context)


# Deletion of a course by the teacher who is its participant (and author)
@teacher_required 
def delete_course(request, course_pk):
    user = request.user 
    try:
        course = user.course_set.get(pk=course_pk) 
    except Course.DoesNotExist: 
        return redirect("teacher_dashboard")

    if request.method == "POST":
        course.delete() 
        return redirect("author_courses") 

    context = {"course": course}
    return render(request, "course/delete_course.html", context) 


# Deletion of a lesson by the teacher
@teacher_required 
def delete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk) 
    course = lesson.course 

    if lesson.course.author != request.user: 
        raise PermissionDenied    

    if request.method == "POST":
        course_id = lesson.course.id 
        lesson.delete() 
        return redirect("edit_course", course_id) 
    context = {"lesson": lesson, "course": course}
    return render(request, "course/delete_lesson.html", context)                                                               


# Adding a course by the teacher
@teacher_required 
def add_course(request):
    if request.method == "POST": 
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False) 
            course.author = request.user
            form.save()
            request.user.courses.add(course) 
            return redirect("my_courses")
    else: 
        form = CourseForm()

    context = {"form": form} 
    return render(request, "course/add_course.html", context)


# Adding a lesson by the teacher               
@teacher_required 
def add_lesson(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)  
    if course.author != request.user: 
        raise PermissionDenied  
    if request.method == "POST": 
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course 
            form.save()
            return redirect("edit_course", course_pk)  
    else:
        form = LessonForm() 

    context = {"form": form} 
    return render(request, "course/add_lesson.html", context)


# Grading a quiz completed by a student
@student_required 
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    course = quiz.lesson.course
    if not Enrollment.objects.filter(user=request.user, course=course).exists(): 
        raise PermissionDenied                                                    
    questions = quiz.question_set.all() 
    total_questions = questions.count() 
    score = 0 

    if request.method == "POST":
        print(request.POST) 
        for question in questions:
            correct_answers = question.answers.filter(is_correct=True).values_list("id", flat=True) 
            print(correct_answers) 
            selected_answers = request.POST.getlist(f"question_{question.id}") 
            print(selected_answers) 
            correct_set = set(correct_answers)
            selected_set = set(map(int, selected_answers)) 
            if correct_set == selected_set:  
                score += 1              

        Results.objects.create(quiz=quiz, user=request.user, score=score, total=total_questions)                                                      
        return redirect("my_results") 

    context = {"quiz": quiz, "questions": questions} 
    return render(request, "course/submit_quiz.html", context)


# Editing the content of a lesson, including the article and quiz, by the teacher                                         
@teacher_required 
def edit_lesson(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk) 
    if lesson.course.author != request.user: 
        raise PermissionDenied  

    article, article_created = Article.objects.get_or_create(lesson=lesson) 
    quiz, quiz_created = Quiz.objects.get_or_create(lesson=lesson) 
    questions = Question.objects.filter(quiz=quiz) 

    if request.method == "POST": 
        article_form = ArticleForm(request.POST, instance=article, prefix="article")
        quiz_form = QuizForm(request.POST, instance=quiz, prefix="quiz")
        lesson_form = LessonForm(request.POST, instance=lesson, prefix="lesson")

        if article_form.is_valid() and quiz_form.is_valid() and lesson_form.is_valid():
            article_form.save()
            quiz_form.save()
            lesson_form.save()
            return redirect("edit_course", lesson.course.pk) 
                                                            
    else: 
        article_form = ArticleForm(instance=article, prefix="article")
        quiz_form = QuizForm(instance=quiz, prefix="quiz")
        lesson_form = LessonForm(instance=lesson, prefix="lesson")

    context = {
        "lesson": lesson,
        "lesson_form": lesson_form,
        "article_form": article_form,
        "quiz_form": quiz_form,
        "questions": questions,
    }
    return render(request, "course/edit_lesson.html", context)


# Adding or editing a question by the teacher 
@teacher_required 
def add_or_edit_question(request, lesson_pk, question_pk=None):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    quiz = get_object_or_404(Quiz, lesson=lesson)    
    if lesson.course.author != request.user:  
        raise PermissionDenied  

    if question_pk:
        question = get_object_or_404(Question, pk=question_pk, quiz=quiz)
    else: 
        question = None

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.quiz = quiz 
            new_question.save()
            return redirect("edit_lesson", lesson_pk=lesson.pk)
    else:
        form = QuestionForm(instance=question)

    context = {
        "lesson": lesson,
        "form": form,
        "is_edit": question is not None, 
    }
    return render(request, "course/add_or_edit_question.html", context)


# Removing a question by the teacher
@teacher_required 
def delete_question(request, lesson_pk, question_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk) 
    if lesson.course.author != request.user: 
        raise PermissionDenied  

    question = get_object_or_404(Question, pk=question_pk)
    question.delete() 

    return redirect("edit_lesson", lesson_pk=lesson_pk)


# Adding or editing an answer by the teacher
@teacher_required 
def add_or_edit_answer(request, lesson_pk, question_pk, answer_pk=None):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)   
    question = get_object_or_404(Question, pk=question_pk) 
    if lesson.course.author != request.user: 
        raise PermissionDenied  

    if answer_pk: 
        answer = get_object_or_404(Answer, pk=answer_pk, question=question) 
    else: 
        answer = None
    if request.method == "POST": 
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid(): 
            new_answer = form.save(commit=False)
            new_answer.question = question 
            new_answer.save()
            return redirect("edit_lesson", lesson_pk=lesson.pk) 
    else: 
        form = AnswerForm(instance=answer)

    context = {
        "lesson": lesson,
        "question": question,
        "form": form,
        "is_edit": answer is not None,  
    }                             
    return render(request, "course/add_or_edit_answer.html", context)


# Deleting an answer by the teacher
@teacher_required 
def delete_answer(request, lesson_pk, answer_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk) 
    if lesson.course.author != request.user: 
        raise PermissionDenied                         
    answer = get_object_or_404(Answer, pk=answer_pk) 
    answer.delete() 

    return redirect("edit_lesson", lesson_pk=lesson_pk) 