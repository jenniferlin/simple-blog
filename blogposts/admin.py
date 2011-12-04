from blogposts.models import Blogpost
from django.contrib import admin
from django.contrib.comments.admin import *

# class CommentInline(admin.TabularInline):
#     model = CommentsAdmin
#     extra = 1
    
class BlogpostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['title']}),
        ('Date information',{'fields': ['pub_date'], 'classes':['collapse']}),
        ('Body',            {'fields': ['body']}),
    ]
    # inlines = [CommentInline]
    list_display = ('title', 'author', 'pub_date','was_published_today')
    list_filter = ['pub_date']
    search_fields = ['title', 'body']
    date_hierarchy = 'pub_date'

admin.site.register(Blogpost, BlogpostAdmin)
