from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,Comment,Contact
from django.utils import timezone
from .forms import PostForm,CommentForm,ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
# Create your views here.

def post_list(request):
	posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request,'blog/post_list.html',{'posts':posts})
	
def post_detail(request,pkk):
	post=get_object_or_404(Post,pk=pkk)
	return render(request, 'blog/post_detail.html',{'post':post})

@login_required
def post_new(request):
	if request.method=='POST':
		form=PostForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			return redirect('post_detail',pkk=post.pk)
	else:
		form=PostForm()
	return render(request,'blog/post_edit.html',{'form':form})

@login_required	
def post_edit(request,pk):
	post=get_object_or_404(Post,pk=pk)
	if request.method=='POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail',pkk=post.pk)
	else:
		form=PostForm(instance=post)
	return render(request,'blog/post_edit.html',{'form':form})
	
@login_required
def post_draft_list(request):
	post=Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request,'blog/post_draft_list.html',{'posts':post})

@login_required	
def post_publish(request, pk):
	post=get_object_or_404(Post,pk=pk)
	post.publish()
	return redirect('post_detail', pkk=pk)

@login_required	
def post_remove(request, pk):
	post=get_object_or_404(Post,pk=pk)
	post.delete()
	return redirect('post_list')
	
def add_comment_to_post(request,pk):
	post=get_object_or_404(Post,pk=pk)
	if request.method=="POST":
		form=CommentForm(request.POST)
		if form.is_valid():
			comment=form.save(commit=False)
			comment.post=post
			comment.save()
			return redirect('post_detail',pkk=post.pk)
	
	else:
		form=CommentForm()
	return render(request,'blog/add_comment_to_post.html',{'form':form})
	
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pkk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog.views.post_detail', pkk=comment.post.pk)
	
def contact(request):
	if request.method=='POST':
		form=ContactForm(request.POST)
		if form.is_valid():
			contact=form.save(commit=False)
			contact.create()
			contact.save()
			return redirect('contact_url')
	else:
		form=ContactForm()
	return render(request,'blog/contact.html',{'form':form})