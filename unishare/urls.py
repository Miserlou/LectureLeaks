from django.conf.urls.defaults import *
from django.conf import settings
#from tastypie.resources import ModelResource
from documents.models import *

#from djangorestframework.views import ListOrCreateModelView, InstanceModelView
#from djangorestframework.resources import ModelResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^captcha/', include('captcha.urls')),
     (r'^unishare/', include('unishare.documents.urls')),
     (r'^upload/', 'unishare.documents.views.upload'),
     (r'^uploadnocaptcha/', 'unishare.documents.views.uploadnocaptcha'),
     (r'^about/', 'unishare.documents.views.about'),
     (r'^apps/', 'unishare.documents.views.apps'),
     (r'^school/(?P<school>[^/]+)/$', 'unishare.documents.views.school'),
     (r'^school/(?P<school>[^/]+)/subject/(?P<subject>[^/]+)/$', 'unishare.documents.views.school_subject'),
     (r'^school/(?P<school>[^/]+)/subject/(?P<subject>[^/]+)/course/(?P<course>[^/]+)/$', 'unishare.documents.views.school_subject_course'),
     #(r'^api/', include('unishare.api.urls')),
     #(r'^api/', include(v2_api.urls) ),
     #(r'^api3/schools',ListOrCreateModelView.as_view(resource=SchoolResource) ),
     #(r'^api3/school/(?P<school>[^/]+)',ListOrCreateModelView.as_view(resource=SubjectResource)),
     #(r'^api3/school/(?P<school>[^/]+)/subject/(?P<subject>[^/]+)',ListOrCreateModelView.as_view(resource=CourseResource) ),
     (r'^api4/schools','unishare.documents.views.api_schools'),
     (r'^api4/school/(?P<school>[^/]+)/$','unishare.documents.views.api_school_subjects'),
     (r'^api4/school/(?P<school>[^/]+)/subject/(?P<subject>[^/]+)/$','unishare.documents.views.api_school_subject_courses'),
     (r'^api4/school/(?P<school>[^/]+)/subject/(?P<subject>[^/]+)/course/(?P<course>[^/]+)/$','unishare.documents.views.api_docs'),

    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'../static'}),
     (r'^uploads/documents/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'../uploads/documents'}),
     (r'^$', 'unishare.documents.views.root')
)
