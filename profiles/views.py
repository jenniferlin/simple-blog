from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.views.generic import list_detail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from profiles.models import *
from profiles.forms import *


@login_required
def profile_detail(request, username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404
    profile = Profile.objects.get(user=user)
    context = { 'object':profile }
    return render_to_response('profiles/profile_detail.html', context, context_instance=RequestContext(request))


@login_required
def profile_edit(request, template_name='profiles/profile_form.html'):
    """Edit profile."""

    if request.POST:
        profile = Profile.objects.get(user=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return HttpResponseRedirect(reverse('profile_detail', kwargs={'username': request.user.username}))
        else:
            context = {
                'profile_form': profile_form,
                'user_form': user_form,
            }
    else:
        try:
            profile = Profile.objects.get(user=request.user)
        except (KeyError, Profile.DoesNotExist):
            #taking care of first time staff user editing profile page
            profile = Profile(user=request.user)
            profile.save()
        context = {
            'profile_form': ProfileForm(instance=profile),
            'user_form': UserForm(instance=request.user),
        }
    return render_to_response(template_name, context, context_instance=RequestContext(request))