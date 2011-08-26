from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from datetime import datetime
from tagging.models import Tag, TaggedItem
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from unishare.documents.models import * 

## Dynamic content

def root(request):
    featureset = School.objects.all().filter(featured=True)
    return render_to_response('all_schools.html', {'schools': featureset, 'cat': 'main', 'recent': get_most_recent()})

def school(request, school):
    schoolo = get_object_or_404(School, name=school)
    featureset = Document.objects.filter(school=schoolo, approved=True).values('subject__name').distinct()
    return render_to_response('by_school.html', {'classes': featureset, 'cat': 'main', 'school': school , 'recent': get_most_recent()})

def school_subject(request, school, subject):
    schoolo = get_object_or_404(School, name=school)
    subjecto = get_object_or_404(Subject, name=subject)
    featureset = Document.objects.filter(school=schoolo, subject=subjecto, approved=True).values('course__name').distinct()
    return render_to_response('by_school_subject.html', {'classes': featureset, 'cat': 'main', 'school': school, 'subject': subject, 'recent': get_most_recent()})

def school_subject_course(request, school, subject, course):
    schoolo = get_object_or_404(School, name=school)
    subjecto = get_object_or_404(Subject, name=subject)
    courseo= get_object_or_404(Course, name=course)
    featureset = Document.objects.all().filter(school=schoolo, subject=subjecto, course=courseo, approved=True).order_by('name')
    return render_to_response('by_school_course.html', {'documents': featureset, 'cat': 'main', 'school': school, 'course': course , 'recent': get_most_recent()})

## Forms ##

def upload(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DocumentForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # XXX: Check filetypes, etc

            form.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = DocumentForm() # An unbound form

    return render_to_response('upload.html', {
        'form': form,
        'cat': 'upload' ,
        'recent': get_most_recent()
    }, context_instance=RequestContext(request))

@csrf_exempt
def uploadnocaptcha(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DocumentNoCaptchaForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # XXX: Check filetypes, etc

            form.save()
            return HttpResponseRedirect('/') # Redirect after POST
        else:
            print form.errors
            print "Shiiiiit"
    else:
        form = DocumentNoCaptchaForm() # An unbound form

    return render_to_response('upload_nocaptcha.html', {
        'form': form,
        'cat': 'upload' ,
        'recent': get_most_recent()
    }, context_instance=RequestContext(request))

## Static ##
def about(request):
    return render_to_response('about.html', {'cat': 'about' , 'recent': get_most_recent()})

def apps(request):
	return render_to_response('apps.html', {'cat': 'apps' , 'recent': get_most_recent()})

def contact(request):
    return render_to_response('contact.html', {'cat': 'contact' , 'recent': get_most_recent()})

## API ##

def api_schools(request):
    json = serializers.get_serializer("json")()
    return HttpResponse(json.serialize(School.objects.all().filter(featured=True), ensure_ascii=False))

def api_school_subjects(request, school):
    json = serializers.get_serializer("json")()
    schoolo = get_object_or_404(School, name=school)
    to_serialize = Document.objects.filter(school=schoolo, approved=True).values('subject__name').distinct()
    return HttpResponse(str(to_serialize))

def api_school_subject_courses(request, school, subject):
    json = serializers.get_serializer("json")()
    schoolo = get_object_or_404(School, name=school)
    subjecto= get_object_or_404(Subject, name=subject)
    to_serialize = Document.objects.filter(school=schoolo, approved=True).filter(subject=subjecto).values('course__name').distinct()
    return HttpResponse(str(to_serialize))

def api_docs(request, school, subject, course):
    json = serializers.get_serializer("json")()
    schoolo = get_object_or_404(School, name=school)
    subjecto= get_object_or_404(Subject, name=subject)
    courseo = get_object_or_404(Course, name=course)
    to_serialize = Document.objects.filter(school=schoolo, approved=True).filter(subject=subjecto).filter(course=courseo)
    return HttpResponse(json.serialize(to_serialize))

##Helper methods ##

def get_most_recent():
    return Document.objects.order_by('-date').filter(approved=True)[:5]

def lookup_or_create(name, cls):
    try:
        obj = cls.objects.get(name=name)
    except cls.DoesNotExist:
        obj = cls(name=name)
        obj.save()
    return obj
