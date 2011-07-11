from tastypie.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from django.shortcuts import get_object_or_404, render_to_response
from tastypie import fields
from documents.models import * 

class SchoolResource(ModelResource):
    school = fields.ToOneField('documents.api.DocResource', 'school')
    
    class Meta:
            queryset = School.objects.all()
            resource_name = 'school'

class SubjectResource(ModelResource):
    class Meta:
            queryset = Subject.objects.all()
            resource_name = 'subject'

   # def dispatch(self, request_type, request, **kwargs):
   #     school_name = request.GET.get('school')
   #     self.derp = get_object_or_404(School, id=school_name)
   #     return super(SubjectResource, self).dispatch(request_type, request, **kwargs)

class CourseResource(ModelResource):
    class Meta:
            queryset = Course.objects.all()
            resource_name = 'course'

class DocResource(ModelResource):
    #school = fields.ForeignKey(SchoolResource, 'school')
    #subject = fields.ForeignKey(SubjectResource, 'subject')
    subject = fields.ToManyField('documents.api.SubjectResouce', 'subject', full=True) 
    school = fields.ToManyField('documents.api.SchoolResouce', 'school', full=True) 
    course= fields.ToManyField('documents.api.CourseResouce', 'course', full=True) 
    #course = fields.ForeignKey(CourseResource, 'course')
   
    def dispatch(self, request_type, request, **kwargs):
        school_name = request.GET.get('school')
        self.derp = get_object_or_404(School, id=school_name)
        return super(SubjectResource, self).dispatch(request_type, request, **kwargs)

    class Meta:
            queryset = Document.objects.all()
            resource_name = 'doc'
            filtering = {
                'school': ALL_WITH_RELATIONS,
                'subject': ALL_WITH_RELATIONS,
                'course': ALL_WITH_RELATIONS,
            }
