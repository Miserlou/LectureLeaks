from django.conf.urls.defaults import *
from piston.resource import Resource
from unishare.api.handlers import DocumentHandler

doc_handler = Resource(DocumentHandler)

urlpatterns = patterns('',
   url(r'^doc/(?P<doc_id>[^/]+)/', doc_handler),
   url(r'^docs/', doc_handler),
)
