
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', blank=True)
    pub_date = models.DateField()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='questions',
        null=True,
        blank=True
    )
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class ExamAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
