from django.contrib import admin
from unishare.documents.models import * 

admin.site.register(Document)
admin.site.register(Course)
admin.site.register(School)
admin.site.register(Subject)

