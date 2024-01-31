from django.contrib import admin
from .models import Subject, Course, Module

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
    
class ModuleInline(admin.StackedInline):
    model = Module
    
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created')
    list_filter = ('created', 'subject')
    # so that we can search over the courses
    search_fields = ('title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    # adding the module model to the course model
    raw_id_fields = ('owner',)
    inlines = [ModuleInline]