from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment, Rating

'''
Class for the Create User Form that contains fields for input of sign up information through HTML.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class CreateUserForm(UserCreationForm):
	password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'text', 'placeholder': 'Password'}))
	password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'textl', 'placeholder': 'Confirm Password'}))
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

		widgets = {
			'username' : forms.TextInput(attrs={'class' : 'text', 'type' : "text", 'placeholder' : 'Username'}),
			'first_name' : forms.TextInput(attrs={'class' : 'text', 'type' : "text", 'placeholder' : 'First Name'}),
			'last_name' : forms.TextInput(attrs={'class' : 'text', 'type' : "text", 'placeholder' : 'Last Name'}),
			'email' : forms.TextInput(attrs={'class' : 'text', 'type' : "email", 'placeholder' : 'E-mail'}),
		}

'''
Class for the Create Post Form that contains fields for input of post information through HTML.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class CreatePost(ModelForm):
	class Meta:
		model = Post
		fields = ['post_title', 'symbol', 'post_text']

		widgets = {
			'post_title' : forms.TextInput(attrs={'class' : 'posttext', 'type' : "posttext", 'placeholder' : 'Title'}),
			'symbol' : forms.TextInput(attrs={'class' : 'symboltext', 'type' : "symboltext", 'placeholder' : ''}),
			'post_text' : forms.Textarea(attrs={'class' : 'area', 'type' : "area",  'placeholder' : 'Body'})
		}

'''
Class for the Create Comment Form that contains fields for input of comment information through HTML.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class CreateComment(ModelForm):
	class Meta:
		model = Comment
		fields = ['post_id', 'user', 'comment']

		widgets = {
			'comment' : forms.Textarea(attrs={'class' : 'comm', 'type' : "comm",  'placeholder' : 'Comment'})
		}