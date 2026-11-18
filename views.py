
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Question, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        'onlinecourse/course_details_bootstrap.html',
        {'course': course}
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method != 'POST':
        return redirect('course_details', course_id=course.id)

    questions = Question.objects.filter(
        lesson__course=course
    ).prefetch_related('choices')

    score = 0
    total_questions = questions.count()
    selected_answers = {}

    for question in questions:
        selected_choice = request.POST.get(
            f'question_{question.id}'
        )

        selected_answers[str(question.id)] = selected_choice

        if selected_choice:
            if question.choices.filter(
                id=selected_choice,
                is_correct=True
            ).exists():
                score += 1

    submission = Submission.objects.create(
        user=request.user,
        course=course,
        score=score
    )

    request.session[f'submission_{submission.id}'] = selected_answers
    request.session[f'total_{submission.id}'] = total_questions

    return redirect(
        'show_exam_result',
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        user=request.user
    )

    questions = Question.objects.filter(
        lesson__course=submission.course
    ).prefetch_related('choices')

    selected_answers = request.session.get(
        f'submission_{submission.id}', {}
    )

    total_questions = request.session.get(
        f'total_{submission.id}', questions.count()
    )

    percentage = (
        (submission.score / total_questions) * 100
        if total_questions else 0
    )

    return render(
        request,
        'onlinecourse/exam_result.html',
        {
            'submission': submission,
            'questions': questions,
            'selected_answers': selected_answers,
            'total_questions': total_questions,
            'percentage': percentage,
        }
    )
