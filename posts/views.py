from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from .models import User, Post, Like, Social
from .forms import PostForm, ProfileForm
from django.db.models import Count, TimeField, DateTimeField
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import TruncDay
from datetime import datetime 
from django.core.serializers import serialize
import os
import json

from geopy.geocoders import Nominatim
# Create your views here.
def index(request):
	return render(request, 'posts/index.html')

def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "posts/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "posts/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))

def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "posts/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "posts/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("editProfile"))
	else:
		return render(request, "posts/register.html")

def allPosts(request):
	user = request.user
	posts = Post.objects.all().order_by('-date','user','-timestamp').exclude(private=True)
	paginator = Paginator(posts, 20)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, "posts/allPosts.html", {
		'posts':posts,
		'user': user
		})

def addThanks(request):
	user = request.user
	posts = Post.objects.filter(user=user).order_by('-timestamp')
	postCount = posts.count()
	userCount =  Post.objects.filter(user=user).annotate(datez=TruncDay('timestamp')).values('datez').annotate(created_count=Count('id')).order_by("-datez")
	if postCount > 0:
		posts = posts[0]
		userCount = userCount[0]['created_count']
	else:
		userCount = 0

	addPost = PostForm(request.POST or None)
	if addPost.is_valid():
		print('VALID!')
		addPost = addPost.save(commit=False)
		addPost.user = request.user
		addPost.timestamp =datetime.now()
		addPost.date =datetime.now()
		addPost.likes = 0
		addPost.save()
		return HttpResponseRedirect(reverse('addThanks'))
	return render(request, "posts/addThanks.html", {
			'postForm': addPost,
			'posts': posts,
			'postCount': postCount,
			'userCount': userCount
		})

def editProfile(request):
	geolocator = Nominatim(user_agent='pk.eyJ1IjoiYmVybmFyZGxhdWdobGluIiwiYSI6ImNrZ254bzh6bTA4dnUycXBmb2x5MnhhZDEifQ.b1d2QwyPmPBNvzrPbMQ5tQ')
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	user =request.user
	initial_data ={
		'first_name': user.first_name,
		'last_name': user.last_name,
		'city': user.city,
		'state': user.state,
		'zip_code': user.zip_code,
		'about': user.about,
		'profile_pic': user.profile_pic,
	}
	currentPic = request.user.profile_pic.url
	currentPic = os.path.join(BASE_DIR, currentPic)
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('profile', user.id)
	else:
		form = ProfileForm(initial=initial_data)
		print('NOT SAVING FORM')
	return render(request, "posts/editProfile.html", {
			'user': user,
			'profile_form': form
		})

def profile(request, id):
	user = get_object_or_404(User, id=id)
	social_ = Social.objects.get(user__username__iexact=user)
	followers_count = user.social.followers.all().count()
	following_count = user.is_following.all().count()
	postCount = Post.objects.filter(user=user).count()
	if request.user in social_.followers.all():
		is_following = True
	else:
		is_following = False
	return render(request, "posts/profile.html",{
			'user': user,
			'is_following': is_following,
			'followers_count': followers_count,
			'following_count': following_count,
			'postCount': postCount
		})

def journal(request):
	user = request.user
	posts = Post.objects.filter(user=user).order_by('-timestamp').values('user','post','timestamp','date')
	#posts_json = serialize("json", list(posts))
	posts = Post.objects.filter(user=user).order_by('-timestamp')
	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, "posts/journal.html", {
		'user':user,
		'posts':posts
		})

def editView(request,post_id):
    post = Post.objects.get(id = post_id)
    print('This is the post to modify')
    print(post)
    oldTime = post.timestamp
    oldDate = post.date
    print(oldTime)
    if request.method == "POST":
        data = json.loads(request.body)
        text = data['text']
        print(text)
        post.post = text
        post.timestamp =oldTime
        post.date = oldDate
        post.save()
    if request.method == "GET":
        return JsonResponse(post.serialize())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def update_follow(request,id):
	user = get_object_or_404(User, id=id)
	social_ = Social.objects.get(user__username__iexact=user)
	if request.method == 'POST':
		if request.user in social_.followers.all():
			social_.followers.remove(request.user)
		else:
			social_.followers.add(request.user)
		update = Social.objects.get(user =request.user)
		update.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def following(request):
	user = request.user
	following = user.is_following.all()
	followers = user.social.followers.all()
	posts = Post.objects.none()
	for i in following:
		followingUser = User.objects.get(username=i)
		p = Post.objects.filter(user = followingUser).order_by('-timestamp').exclude(private=True)
		posts = posts | p

	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, "posts/following.html", {
		'posts': posts
		})

def like_post(request):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data['id']
        post_obj = Post.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def maps(request):
	geolocator = Nominatim(user_agent='pk.eyJ1IjoiYmVybmFyZGxhdWdobGluIiwiYSI6ImNrZ254bzh6bTA4dnUycXBmb2x5MnhhZDEifQ.b1d2QwyPmPBNvzrPbMQ5tQ')
	user = request.user
	allUsers = User.objects.all()
	city = User.city
	state = User.state
	mapbox_access_token = 'pk.my_mapbox_access_token'
	return render(request, "posts/maps.html", {
		'mapbox_access_token': mapbox_access_token,
		'user': user,
		'city':city,
		'state':state,
		'allUsers': allUsers
		})

