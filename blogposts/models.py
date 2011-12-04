from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime
# from django.contrib.comments.models import *

class Blogpost(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    slug = models.SlugField('slug', unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Blogpost, self).save(*args, **kwargs)        
        
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'
    
# class Comment(models.Model):
#     # Who posted this comment? If ``user`` is set then it was an authenticated
#     # user; otherwise at least user_name should have been set and the comment
#     # was posted by a non-authenticated user.
#     user = models.ForeignKey(User, blank=True, null=True)
#     user_name = models.CharField("user's name", max_length=50, blank=True)
#     comment = models.TextField(max_length=3000)
#     submit_date = models.DateTimeField('date/time submitted', default=None)
#     blogpost = models.ForeignKey(Blogpost)
# 
#     def __unicode__(self):
#         return "%s: %s..." % (self.user_name, self.comment[:50])
