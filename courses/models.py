from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('title',)
        
    def __str__(self):
        return self.title
    
    
class Course(models.Model):
    
    # user.courses_created.all()
    # course.user.username
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='courses_created')
    
    # subject.courses.all()
    # course.subject.title
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    # time the course was created.
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # most recent courses at the top
        ordering = ('-created',)
        
    def __str__(self):
        return self.title
    
    
    

class Module(models.Model):
    # course.modules.all()
    # module.course.subject.title
    course = models.ForeignKey(Course, 
                               related_name='modules',
                               on_delete=models.CASCADE)
    
    # title of the course.
    title = models.CharField(max_length=200)
    # description of the course.
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    
    def __str__(self):
        return f"{self.order}. {self.title}"
    
    class Meta:
        ordering = ('order',)
    
    
class Content(models.Model):
    # the module the content is related to.
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    
    # points to the model
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file'
                                     )})
    
    # id of the object
    object_id = models.PositiveIntegerField()
    
    # combines the model and the id to point to the object
    item = GenericForeignKey('content_type', 'object_id')
    
    order = OrderField(blank=True, for_fields=['module'])
    
    class Meta:
        ordering = ('order',)
    
    
class ItemBase(models.Model):
    # the owner of the content
    
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.title
    
    
class Text(ItemBase):
    """to store text content"""
    content = models.TextField()
    
class File(ItemBase):
    """to store files, like pdf, excel"""
    file = models.FileField(upload_to='files/%Y/%m/%d')
    
class Image(ItemBase):
    """to store images"""
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    
class Video(ItemBase):
    """to store video content"""
    video = models.URLField()