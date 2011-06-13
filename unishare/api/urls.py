from django.conf.urls.defaults import *
from piston.resource import Resource
from unishare.api.handlers import * 

subject_handler = Resource(SubjectHandler)
schools_handler = Resource(SchoolsHandler)
course_handler = Resource(CourseHandler)
doc_handler = Resource(DocHandler)

urlpatterns = patterns('',
   url(r'^schools/', schools_handler),
   url(r'^school/(?P<school_name>[^/]+)/', subject_handler),
   url(r'^school/(?P<school_name>[^/]+)/subject/(?P<subject_name>[^/]+)', course_handler),
   url(r'^school/(?P<school_name>[^/]+)/subject/(?P<subject_name>[^/]+)/course/(?P<course_name>[^/]+)', doc_handler),
)
