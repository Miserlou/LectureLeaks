from piston.handler import BaseHandler
from django.shortcuts import get_object_or_404
from documents.models import * 

class SubjectHandler(BaseHandler):
   allowed_methods = ('GET',)
   fields = ('subject',) ## That comma is really important
   model = Document 

   def read(self, request, school_name=None):
       base = Document.objects
       if school_name:
           s = get_object_or_404(School, name=school_name)
           return base.filter(school=s)
       else:
           return None 

class CourseHandler(BaseHandler):
   allowed_methods = ('GET',)
   fields = ('course',) ## That comma is really important
   model = Document 

   def read(self, request, school_name=None, subject_name=None):
       base = Document.objects
       if school_name:
           s = get_object_or_404(School, name=school_name)
           c = get_object_or_404(Subject, name=subject_name)
           return base.filter(school=s).filter(subject=c)
       else:
           return None 

class DocHandler(BaseHandler):
   allowed_methods = ('GET',)
   fields = ('name', 'file_loc', ) ## That comma is really important
   model = Document 

   def read(self, request, school_name=None, subject_name=None, course_name=None):
       base = Document.objects
       
       if school_name not None and subject_name is None and course_name is None:
           s = get_object_or_404(School, name=school_name)
           return base.filter(school=s)
       if school_name not None and subject_name not None and course_name is None:
           s = get_object_or_404(School, name=school_name)
           return base.filter(school=s)
        
       if not 

       if school_name:
           s = get_object_or_404(School, name=school_name)
           c = get_object_or_404(Subject, name=subject_name)
           d = get_object_or_404(Course, name=course_name)
           return base.filter(school=s).filter(subject=c).filter(course=d)
       else:
           return None 

class SchoolsHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = School 
