from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime

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
    
