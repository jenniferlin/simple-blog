import re, datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField

class Profile(models.Model):
    """Profile model"""
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    user = models.ForeignKey(User, unique=True)
    gender = models.PositiveSmallIntegerField('gender', choices=GENDER_CHOICES, blank=True, null=True)
    address1 = models.CharField(_('address1'), blank=True, max_length=100)
    address2 = models.CharField(_('address2'), blank=True, max_length=100)
    city = models.CharField(_('city'), blank=True, max_length=100)
    state = models.CharField(_('state'), blank=True, max_length=100)
    zip = models.CharField(_('zip'), blank=True, max_length=10)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        db_table = 'user_profiles'

    def __unicode__(self):
        return u"%s" % self.user.get_full_name()

    @permalink
    def get_absolute_url(self):
        return ('profile_detail', None, { 'username': self.user.username })

