from blogposts.models import Blogpost
from django.contrib.comments.models import Comment
from django.contrib.comments.forms import CommentForm
from blogposts.forms import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from functools import wraps
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from django.http import HttpResponse
# from django.template import Context, loader
from django.contrib.admin.views import decorators
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME
def staff_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)
        else:
            defaults = {
                'template_name': 'login.html',
                'authentication_form': AdminAuthenticationForm,
                'extra_context': {
                    'title': 'Log in',
                    'app_path': request.get_full_path(),
                    REDIRECT_FIELD_NAME: request.get_full_path(),
                },
            }
            return login(request, **defaults)
    return wraps(view_func)(_checklogin)

decorators.staff_member_required = staff_member_required

def index(request):
    blogs = Blogpost.objects.all().order_by('-pub_date')
    paginator = Paginator(blogs, 5) 

    page = request.GET.get('page',1)
    try:
        blogposts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogposts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogposts = paginator.page(paginator.num_pages)

    return render_to_response('blogposts/index.html', {"blogposts": blogposts})
        
    # latest_blog_list = Blogpost.objects.all().order_by('-pub_date')[:5]
    # t = loader.get_template('blogposts/index.html')
    # c = Context({
    #     'latest_blog_list': latest_blog_list,
    # })
    # return HttpResponse(t.render(c))
    # return render_to_response('blogposts/index.html',{'latest_blog_list': latest_blog_list},
    #                           context_instance=RequestContext(request))
    
def detail(request, slug):
    blog = get_object_or_404(Blogpost, slug=slug)
    # data =dict()
    # if request.user.is_authenticated():
    #     data["name"] = request.user.get_full_name() or request.user.username
    # if request.user.is_authenticated():
    #     print "in detail..user is authenticated"
    #     c.user_name = request.user.get_full_name() or request.user.username
    #     c.user = request.user
    # form = CommentForm(c)
    # form.name = request.user.get_full_name() or request.user.username
    # form = CommentForm(Comment(), data=data)
    return render_to_response('blogposts/detail.html', {'blogpost':blog, 'form':CommentForm(blog)},
                              context_instance=RequestContext(request))
                              

def comment_create(request, slug, template_name='blogposts/detail.html'):
    blog = get_object_or_404(Blogpost, slug=slug)
    comment = Comment(pk=blog.id, user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogposts.views.detail', args=(blog.slug,)))
    else:
        form = CommentForm(instance=comment)
        
    context = { 'form': form,
                'comment' : comment}
    return render_to_response(template_name, context, context_instance=RequestContext(request))
    
@staff_member_required
def create_or_edit(request, slug=None, template_name='blogposts/form.html'):
    if slug: # edit existing blogpost
        blog = get_object_or_404(Blogpost, slug=slug)
        form_action = '/blogposts/%s/edit/'%slug
    else: # create new blogpost
        blog = Blogpost()
        form_action = '/blogposts/create/'
    
    if request.POST:
        blog.author = request.user
        if not slug:
            blog.pub_date = datetime.now()
        blogpost_form = BlogpostForm(request.POST, request.FILES, instance=blog)
        if blogpost_form.is_valid():
            blogpost_form.save()
            return HttpResponseRedirect(reverse('blogposts.views.detail', args=(blog.slug,)))
            
    context = { 'blogpost_form': BlogpostForm(instance=blog),
                'form_action' : form_action}
    return render_to_response(template_name, context, context_instance=RequestContext(request))
                                  
# @staff_member_required
# def create(request, template_name='blogposts/form.html'):
#     print "in create"
#     if request.POST:
#         blog = Blogpost()
#         print "I m here!!! in post"
#         blogpost_form = BlogpostForm(request.POST, request.FILES, instance=blog)
#         if blogpost_form.is_valid():
#             blogpost_form.save()
#             return HttpResponseRedirect(reverse('blogposts.views.detail', args=(slug,)))
#             
#     context = { 'blogpost_form': BlogpostForm() }
#     return render_to_response(template_name, context, context_instance=RequestContext(request))
                                  
def comment(request):
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    blog = get_object_or_404(Blogpost, pk=data['blogpost_id'])
    
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.username
    
    if request.method == 'POST':
        form = CommentForm(data=data)
        if form.is_valid():
            comment = form.get_comment_object()
            if request.user.is_authenticated():
                comment.user = request.user
            comment.blogpost = blog
            comment.save()
            return HttpResponseRedirect(reverse('blogposts.views.detail', args=(blog.id,)))
    return render_to_response('blogposts/detail.html', {'blogpost':blog, 'comment_list':blog.comment_set.all(), 'form':form},
                                context_instance=RequestContext(request))            
    
