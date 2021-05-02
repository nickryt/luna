from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from .decorators import *
from django.conf import settings
import json
import datetime
import requests
import os

'''
Contains all functions that deal with HTML page information and page redirection.
A "view function" is a function that sends the HTML page to the client.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
finnhubtoken = '&token=c0j032n48v6rb22ahmkg'
pricequery = 'https://finnhub.io/api/v1/quote?symbol='

'''
View function to build the data for the home page.
Queries stock information from posts made for the carousel.

@param HTTP request
@return Renders the home page for the website
'''
def home(request):
    post_dump = Post.objects.all()
    vote_counts = []
    comment_counts = []
    dates_created = []
    voted_on = []
    stocknames = []
    stockprices = []
    lowprices = []
    highprices = []

    for individual in post_dump:
        post_info = get_post_info(individual)
        vote_counts.append(post_info['total_votes'])
        comment_counts.append(post_info['total_post_comments'])
        dates_created.append(post_info['thisdate'])
        voted_on.append(findVote(request, individual.post_id))

    # QUERY FOR HOT STOCKS CAROUSEL
    # PULLING LAST TICKER FROM DB 
    print('\n|--------------------------------------| QUERY START |--------------------------------------|')
    latestposts = Post.objects.all().order_by('-post_id')[:30]

    for item in latestposts:
        currentticker = item.symbol
        if len(stocknames) == 8:
            print('STOCKS TO QUERY : ' + str(stocknames))
            break
        if currentticker not in stocknames: # AVOIDING DUPLICATES
            stocknames.append(currentticker)
    # print(stocknames)

    for item in stocknames:
        try:
            getquote = requests.get(pricequery + str(item) + finnhubtoken)
            getquote = getquote.json()
            print('Executed Price Query : ' + str(getquote))
            stockprices.append(getquote['c'])
            lowprices.append(getquote['l'])
            highprices.append(getquote['h'])
        except KeyError:
            print("Count Not Execute Price Query")
            stockprices.append('0')
            lowprices.append('0')
            highprices.append('0')
            return redirect("error_page")

    print('|--------------------------------------| QUERY END |--------------------------------------|\n')

    context = {
        'post_dump' : post_dump, 'vote_counts' : vote_counts, 'comment_counts' : comment_counts, 'dates_created' : dates_created,
        'voted_on' : voted_on, 'stocknames' : stocknames, 'stockprices' : stockprices, 'lowprices' : lowprices, 'highprices' : highprices
    }

    return render(request, 'accounts/home.html', context)

'''
View function to build the data for the profile page.
Users must be logged in to access the page.

@param HTTP request
@return Renders the login page if unsuccessful, profile page if successful
'''
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['access', 'admin'])
def profile(request):
    if not request.user.is_authenticated:
       return redirect('login_page')

    post_dump = Post.objects.filter(user=request.user)
    acct = Account.objects.filter(user=request.user)
    vote_counts = []
    comment_counts = []
    dates_created = []

    # retrieves user data from the database
    for individual in post_dump:
        post_info = get_post_info(individual)
        vote_counts.append(post_info['total_votes'])
        comment_counts.append(post_info['total_post_comments'])
        dates_created.append(post_info['thisdate'])

    context = {
        'acct' : acct[0],
        'post_dump' : post_dump,
        'vote_counts' : vote_counts,
        'comment_counts' : comment_counts,
        'dates_created' : dates_created
    }

    return render(request, 'accounts/profile.html', context)

'''
View function to build the data for the profile settings page.
Users must be logged in to access the page.

@param HTTP request
@param Error message
@return Renders the profile settings page for the website
'''
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['access', 'admin'])
def profilesettings(request, err=""):
    acct = Account.objects.filter(user=request.user)
    pics = os.listdir(os.path.join(settings.MEDIA_ROOT, "img/"))
    half1 = int(len(pics)/2)
    half2 = len(pics) - half1
    context = {
        'acct' : acct[0],
        'pics1' : pics[:half1],
        'pics2' : pics[-half2:],
        'pics' : pics
    }
    return render(request, 'accounts/profilesettings.html', context)

'''
View function to build the data for the update profile page.

@param HTTP request
@return Request to redirect to profile page
'''
def updateprofile(request):
    acct = Account.objects.filter(user=request.user)

    # gets user and account data for the page
    if request.method == "POST":
        fname = request.POST.get('account-fn')
        lname = request.POST.get('account-ln')
        avatr = request.POST.get('avatar')
        abtme = request.POST.get('account-abt')

        user = User.objects.filter(username = request.user.username)
        user.update(first_name=fname)
        user.update(last_name=lname)

        acct.update(about_me=abtme)
        if avatr != "" :
            acct.update(profile_picture=avatr)

    return redirect('profile_page')

'''
View function to delete a user from the database.

@param HTTP request
@return Request to redirect to the home page
'''
def deleteprofile(request):
    u = User.objects.get(username = request.user.username)
    logout(request)
    u.delete()
    return redirect('homepage')

'''
View function to allow an unauthenticated user to log into Luna.

@param HTTP request
@return Renders the login page, redirect to profile page if log in was successful
'''
@unauthenticated_user
def login_page(request):
    username = request.POST.get('fname')
    password = request.POST.get('psswd')

    # First load of log in page, form not filled out
    if username == None or password == None :
        return render(request, 'accounts/login.html', {'err' : False})

    # Authenticate user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('profile_page')
    else:
        return render(request, 'accounts/login.html', {'err' : True})

'''
View function to log user out of Luna web application.

@param HTTP request
@return Request to redirect to login page
'''
def log_out(request) :
    logout(request)
    return redirect("login_page")

'''
View function to allow an unauthenticated user to create an account.

@param HTTP request
@return Renders the signup page, redirect to login page if creation successful
'''
@unauthenticated_user
def signup(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Creates a Django User
            newuser = form.save()
            print('\nForm Saved')

            # Creates an Accounts object using the Django User
            username = form.cleaned_data.get('username')
            obj = User.objects.get(username = username)
            group = Group.objects.get(name = 'access')
            newuser.groups.add(group)

            acct = Account(user=obj)
            acct.save()
            
            messages.success(request, 'Account was created for ' + username)

            return redirect('login_page')
        else:
            print('\nForm Failed')
            messages.error(request, 'Creation failed')

            # gets the error list from the form
            err = form.errors
            print(err)
            iterator = iter(err.values())
            first = f'{next(iterator)}'
            print(first)

            # determines error type
            if first.find('username already exists') != -1:
                context = {'form':form, 'user':True}
            elif first.find('password is too short') != -1:
                context = {'form':form, 'short':True}
            elif first.find('password is too common') != -1:
                context = {'form':form, 'comm':True}
            elif first.find('two password fields') != -1:
                context = {'form':form, 'two':True}
            else:
                context = {'form':form, 'err':True}

            return render(request, 'accounts/signup.html', context)

    context = {'form':form}
    return render(request, 'accounts/signup.html', context)

'''
View function to build the data for the stock page.

@param HTTP request
@return Renders the stock page for the website
'''
def stock(request):
    ticker = request.GET.get("stock")
    post_dump = Post.objects.filter(symbol=ticker)
    vote_counts = []
    comment_counts = []
    dates_created = []
    voted_on = []

    # gets the post information fro the stock ticker
    for individual in post_dump:
        post_info = get_post_info(individual)
        vote_counts.append(post_info['total_votes'])
        comment_counts.append(post_info['total_post_comments'])
        dates_created.append(post_info['thisdate'])
        voted_on.append(findVote(request, individual.post_id))

    context = {
        'ticker' : ticker, 'post_dump' : post_dump, 'vote_counts' : vote_counts,
        'voted_on' : voted_on, 'comment_counts' : comment_counts, 'dates_created' : dates_created
    }

    return render(request, 'accounts/stock.html', context)

'''
View function to allow users to create a new post.
Users must be logged in to access the page.

@param HTTP request
@return Renders the stock page for the website
'''
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['access', 'admin'])
def newpost(request):
    form = CreatePost(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit = False)
            obj.user = request.user
            obj.save()
            form = CreatePost()
            print('Created Post : ' + str(obj.post_id))
            key = str(obj.post_id)
            return redirect(viewpost, key)

    context = {'form':form}
    return render(request, 'accounts/newpost.html', context)

'''
View function to allow users to create a new post.
Users must be logged in to access the page.

@param HTTP request
@return Renders the stock page for the website
'''
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['access', 'admin'])
def viewpost(request, post_key):
    # GET POST
    thispost = Post.objects.get(post_id=post_key)
    context = get_post_info(thispost, post_key)
    form = CreateComment(request.POST)
    voted_on = findVote(request, post_key)

    if request.method == "POST":

        # GETS COMMENTS ON POST
        for field in form.fields:
            if field == 'comment':
                form.fields[field].required = True
                if form.data['comment'].isspace():
                    return HttpResponseRedirect(str(post_key))
            else:
                form.fields[field].required = False
        form.save(commit = False)

        # CREATES NEW COMMENT FOR POST
        if form.is_valid():
            print("IS VALID ")
            obj = form.save(commit = False)
            obj.user = request.user
            obj.post_id = thispost
            obj.save()
            form = CreateComment()
            return HttpResponseRedirect(str(post_key))

    context['form'] = form
    context['voted_on'] = voted_on
    return render(request, 'accounts/viewpost.html', context) 

'''
Retrieves a post object from the database and creates a dictionary from the data.
If no post is passed in, defaults to zero.

@param Post object
@param Default post key
@return Dictionary of post information for thispost
'''
def get_post_info(thispost, post_key=0) :
    # CALCULATE POST VOTE COUNT
    all_votes = thispost.rating_set.all().count()
    upvotes = thispost.rating_set.filter(vote='UPVOTE').count()
    downvotes = thispost.rating_set.filter(vote='DOWNVOTE').count()
    total_votes = upvotes - downvotes

    # CALCULATE POST COMMENT COUNT
    total_post_comments = thispost.comment_set.all().count()

    # QUERY FOR DATE OF POST CREATION
    thisdate = thispost.post_date_created
    thisdate = thisdate.strftime("%x") # FORMAT DATE

    # PULL ALL COMMENTS FROM DATABASE
    allcomments = thispost.comment_set.filter(post_id=post_key)
    post_info = {
        'thispost' : thispost, 'total_votes' : total_votes, 'total_post_comments' : total_post_comments,
        'thisdate' : thisdate, 'allcomments' : allcomments, 'post_key' : post_key
    }

    return post_info

'''
Deletes the selected post from the database.

@param HTTP request
@param Post ID number
@return Request to redirect to home page
'''
def deletepostredirect(request, post_key):
    beingdeleted = Post.objects.get(post_id=post_key)
    beingdeleted.delete()
    return redirect('homepage')

'''
Deletes the selected comment from the database.

@param HTTP request
@param Comment ID number
@param Post ID number
@return Request to redirect to view post page
'''
def deletecommentredirect(request, comment_key, post_key):
    beingdeleted = Comment.objects.get(id=comment_key)
    beingdeleted.delete()
    return redirect('view_post', post_key)

'''
Creates a rating object in the database for a given post.

@param HTTP request
@param Post ID number
@param ID number of user voting
@param User's upvote or downvote
@return Renders the login page if unauthenticated, else redirects to the view post page of post key
'''
def createVote(request, post_key, user_id, voted):
    if request.user.is_authenticated:
        fetchedID = Post.objects.get(post_id=post_key)
        fetchedAccount = Account.objects.get(account_id=user_id)
        try:
            findRating = Rating.objects.get(post=fetchedID, user=fetchedAccount)
            print(findRating)
            # the rating is the same (ex. UPVOTE and UPVOTE)
            if(findRating.vote == voted):
                findRating.delete()
            else: 
                # changes stored vote to new vote
                findRating.vote = voted
                findRating.save()
        except Rating.DoesNotExist:
            # creates new rating for post and user
            VoteObject = Rating(post=fetchedID, user=fetchedAccount, vote=voted)
            VoteObject.save()
            print(VoteObject)
        return redirect('view_post', post_key)
    else:
        return render(request, 'accounts/login.html')

'''
Searches for the current user's rating on a given post.

@param HTTP request
@param Post ID number
@return Returns rating of current user, NONE otherwise
'''
def findVote(request, post_key):
    fetchedID = Post.objects.get(post_id=post_key)
    currentuser = request.user
    if request.user.is_authenticated:
        fetchedAccount = Account.objects.get(user=currentuser)
        try:
            findRating = Rating.objects.get(post=fetchedID, user=fetchedAccount)
            return findRating.vote

        except Rating.DoesNotExist:
            return 'NONE'
    return 'NONE'