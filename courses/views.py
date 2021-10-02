from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.

from .models import Course

def index(request):
    return render(request, "courses/index.html", {
        "courses": Course.objects.all()
    })


def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    return render(request, "courses/course.html", {
        "course": course,
        "students": course.students.all()
    })


def book(request, course_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("users:login")+f"?next={request.path}")

    course = get_object_or_404(Course, pk=course_id)
    if request.user not in course.students.all():
        course.students.add(request.user)
        course = Course.objects.get(id = course_id)
        course.nowquantity += 1
        course.save()
    return HttpResponseRedirect(reverse("courses:course", args=(course_id,)))


def remove(request, course_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login")
        return HttpResponseRedirect(reverse("users:login")+f"?next={request.path}")

    course = get_object_or_404(Course, pk=course_id)
    if request.user in course.students.all():
        course.students.remove(request.user)
        course = Course.objects.get(id = course_id)
        course.nowquantity -= 1
        course.save()
    return HttpResponseRedirect(reverse("courses:course", args=(course_id,)))


def godhand(request, course_id):
    if request.user.is_superuser:
        course = Course.objects.get(id = course_id)
        if course.status:
            course.status = False
            course.save()
        else:
            course.status = True
            course.save()
    return HttpResponseRedirect(reverse("courses:course", args=(course_id,)))

