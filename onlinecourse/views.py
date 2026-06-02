from .models import Submission, Choice, Course, Enrollment
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


# -----------------------------
# AUTH
# -----------------------------
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

    username = request.POST['username']
    password = request.POST['psw']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']

    if User.objects.filter(username=username).exists():
        context['message'] = "User already exists."
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password
    )
    login(request, user)
    return redirect("onlinecourse:index")


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)

    return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


# -----------------------------
# HELPERS
# -----------------------------
def check_if_enrolled(user, course):
    if not user.is_authenticated:
        return False
    return Enrollment.objects.filter(user=user, course=course).exists()


# -----------------------------
# COURSE VIEWS
# -----------------------------
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]

        for course in courses:
            course.is_enrolled = check_if_enrolled(user, course)

        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


# -----------------------------
# ENROLL
# -----------------------------
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if user.is_authenticated and not check_if_enrolled(user, course):
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(
        reverse('onlinecourse:course_details', args=(course.id,))
    )


# -----------------------------
# EXTRACT ANSWERS
# -----------------------------
def extract_answers(request):
    selected = []
    for key in request.POST:
        if key.startswith('choice'):
            selected.append(int(request.POST[key]))
    return selected


# -----------------------------
# SUBMIT EXAM
# -----------------------------
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if not user.is_authenticated:
        return redirect('onlinecourse:login')

    enrollment = get_object_or_404(Enrollment, user=user, course=course)

    selected_ids = extract_answers(request)

    submission = Submission.objects.create(enrollment=enrollment)

    for choice_id in selected_ids:
        submission.choices.add(choice_id)

    return redirect('onlinecourse:course_details', course.id)