from blogposts.models import Blogpost
from django.contrib import admin
    
class BlogpostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['title']}),
        ('Date information',{'fields': ['pub_date'], 'classes':['collapse']}),
        ('Body',            {'fields': ['body']}),
    ]
    list_display = ('title', 'author', 'pub_date','was_published_today')
    list_filter = ['pub_date']
    search_fields = ['title', 'body']
    date_hierarchy = 'pub_date'

admin.site.register(Blogpost, BlogpostAdmin)
