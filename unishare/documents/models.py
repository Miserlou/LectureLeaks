from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.forms import ModelForm
from datetime import datetime
from time import time
from django import forms
from django.conf import settings
from tagging.fields import TagField
from tagging.models import Tag
from captcha.fields import CaptchaField
from os.path import splitext

import re

attachment_file_storage = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url='documents')

class School(models.Model):
    name = models.CharField(max_length='200', blank=False, unique=True)
    featured = models.BooleanField(default=False, blank=True)

    def natural_key(self):
        return (self.name)

    def __unicode__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length='200', blank=False, unique=True)

    def __unicode__(self):
        return self.name

    def natural_key(self):
            return (self.name)

class Course(models.Model):
    name = models.CharField(max_length='200', blank=False, unique=True)

    def __unicode__(self):
        return self.name
    
    def natural_key(self):
            return (self.name)

# Create your models here.
class Document(models.Model):

    # Document specific
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School, blank=False)
    course = models.ForeignKey(Course, blank=False)
    subject = models.ForeignKey(Subject, blank=False)
    professor = models.CharField(max_length='200', blank=True)

    # Files specific
    local_file = models.CharField(max_length='200', blank=True)
    doc_file = models.FileField(upload_to='documents', storage=attachment_file_storage)
    file_loc = models.CharField(max_length='200', blank=True)
    mp3_address = models.CharField(max_length='200', blank=True)

    # Meta specific
    date = models.DateTimeField('date uploaded', blank=True, default=datetime.now())
    approved = models.BooleanField(default=False, blank=True)
    featured = models.BooleanField(default=False, blank=True)

    tags = TagField()

    def save(self):
        super(Document, self).save()

        # New recording, let me know about it
        #if not self.approved:
        #    send_mail('New recording: ' + self.name, 'Public: \n ' + self.public_description + 'Private: \n' +         self.private_description, 'bigvagitabluntz420@gmail.com', ['rich@anomos.info'], fail_silently=False)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def __unicode__(self):
        return self.name + ' - ' + self.course.name + ' - ' + self.school.name + ' (' + self.file_loc + ')'

class DocumentNoCaptchaForm(ModelForm):
    school = forms.CharField(max_length=100)
    course = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)

    class Meta:
        model = Document
        exclude = ('school', 'course', 'subject')

    #def __init__(self, bound_object=None, *args, **kwargs):
    #    super(RecordingForm, self).__init__(*args, **kwargs)
    #    self.bound_object = bound_object
    #    self.is_updating = False
    #    if self.bound_object:
    #        self.is_updating = True

    def clean(self):
        doc = self.cleaned_data.get('doc_file',None)
        if doc is None:
            self._errors['doc_file'] = "No file supplied!"
            raise forms.ValidationError('')

        #if doc.size > 2097152000:
        #    self._errors['doc_file'] = "That file is too large."
        #    raise forms.ValidationError('')

        #valid_content_types = ('audio/mpeg', 'audio/x-mpeg', 'audio/mpeg3', 'audio/x-mpeg-3', 'audio/x-caf', 'audio/3gpp')
        #valid_file_extensions = ('3gp', 'mp3', 'caf')

        #ext = splitext(doc.name)[1][1:].lower()
        #if not ext in valid_file_extensions \
        #   and not doc.content_type in valid_content_types:
        #    self._errors['doc_file'] = "Sorry, this is not a valid file-type."
        #    raise forms.ValidationError('')

        return self.cleaned_data

    def save(self):
        self.bound_object = Document()
        uploaded_file = self.cleaned_data['doc_file']
        s_time = str(time())
        s_path = s_time + re.sub(r'[^a-zA-Z0-9._]+', '-', uploaded_file.name)
        stored_name = s_time + re.sub(r'[^a-zA-Z0-9._]+', '-', uploaded_file.name)
        self.bound_object.mimetype = uploaded_file.content_type
        self.bound_object.name = self.cleaned_data['name']
        self.bound_object.school = lookup_or_create(self.cleaned_data['school'].title(), School)
        self.bound_object.course = lookup_or_create(self.cleaned_data['course'].title(), Course)
        self.bound_object.professor = self.cleaned_data['professor']
        self.bound_object.subject = lookup_or_create(self.cleaned_data['subject'], Subject)
        self.bound_object.date = datetime.now()
        self.bound_object.file_loc = settings.UPLOAD_HARD + s_path
        self.bound_object.doc_file.save(stored_name, uploaded_file)
        self.bound_object.save()

class DocumentForm(ModelForm):
    school = forms.CharField(max_length=100)
    course = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)

    captcha = CaptchaField()
    class Meta:
        model = Document
        exclude = ('school', 'course', 'subject')

    #def __init__(self, bound_object=None, *args, **kwargs):
    #    super(RecordingForm, self).__init__(*args, **kwargs)
    #    self.bound_object = bound_object
    #    self.is_updating = False
    #    if self.bound_object:
    #        self.is_updating = True

    def clean(self):
        doc = self.cleaned_data.get('doc_file',None)
        if doc is None:
            self._errors['doc_file'] = "No file supplied!"
            raise forms.ValidationError('')

        #if doc.size > 2097152000:
        #    self._errors['doc_file'] = "That file is too large."
        #    raise forms.ValidationError('')

        #valid_content_types = ('audio/mpeg', 'audio/x-mpeg', 'audio/mpeg3', 'audio/x-mpeg-3', 'audio/x-caf', 'audio/3gpp')
        #valid_file_extensions = ('3gp', 'mp3', 'caf')

        #ext = splitext(doc.name)[1][1:].lower()
        #if not ext in valid_file_extensions \
        #   and not doc.content_type in valid_content_types:
        #    self._errors['doc_file'] = "Sorry, this is not a valid file-type."
        #    raise forms.ValidationError('')

        return self.cleaned_data

    def save(self):
        self.bound_object = Document()
        uploaded_file = self.cleaned_data['doc_file']
        s_time = str(time())
        s_path = s_time + re.sub(r'[^a-zA-Z0-9._]+', '-', uploaded_file.name)
        stored_name = s_time + re.sub(r'[^a-zA-Z0-9._]+', '-', uploaded_file.name)
        self.bound_object.mimetype = uploaded_file.content_type
        self.bound_object.name = self.cleaned_data['name']
        self.bound_object.school = lookup_or_create(self.cleaned_data['school'].title(), School)
        self.bound_object.course = lookup_or_create(self.cleaned_data['course'], Course)
        self.bound_object.professor = self.cleaned_data['professor']
        self.bound_object.subject = lookup_or_create(self.cleaned_data['subject'], Subject)
        self.bound_object.date = datetime.now()
        self.bound_object.file_loc = settings.UPLOAD_HARD + s_path
        self.bound_object.doc_file.save(stored_name, uploaded_file)
        self.bound_object.save()

def lookup_or_create(name, cls):
    try:
        obj = cls.objects.get(name=name)
    except cls.DoesNotExist:
        obj = cls(name=name)
        obj.save()
    return obj

