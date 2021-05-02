from django.test import Client, RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser, User, Group
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import *
from .views import *
from .forms import *

from datetime import datetime

'''
Class that tests the validity of Luna's database models.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class ModelsTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(
			username='testuser',
			email='test@gmail.com',
			first_name='first',
			last_name='last',
			password='testingpass1'
		)

		Account.objects.create(
			account_id=User.objects.get(id=1).id,
			user=User.objects.get(id=1),
			profile_picture=None,
			date_created=None,
			about_me='About me information'
		)

		Post.objects.create(
			post_id = 1,
			symbol='RMTD',
			post_title='Title',
			post_text='Post text',
			post_date_created=None,
			user=User.objects.get(id=1)
		)

		Rating.objects.create(
			post=Post.objects.get(post_id=1),
			user=Account.objects.get(account_id=1),
			vote='UPVOTE'
		)

		Comment.objects.create(
			post_id=Post.objects.get(post_id=1),
			user=User.objects.get(id=1),
			comment='This is a test comment',
			comment_date_created=None
		)

	def test_user_label(self):
		print('\nTesting user labels:')
		test_user = User.objects.get(id=1)

		label = test_user._meta.get_field('username').verbose_name
		self.assertEqual(label, 'username')

		label = test_user._meta.get_field('email').verbose_name
		self.assertEqual(label, 'email address')

		label = test_user._meta.get_field('first_name').verbose_name
		self.assertEqual(label, 'first name')

		label = test_user._meta.get_field('last_name').verbose_name
		self.assertEqual(label, 'last name')

		label = test_user._meta.get_field('password').verbose_name
		self.assertEqual(label, 'password')

	def test_user_values(self):
		print('\nTesting user values:')
		test_user = User.objects.get(id=1)

		obj = f'{test_user.username}'
		self.assertEqual(obj, 'testuser')

		obj = f'{test_user.email}'
		self.assertEqual(obj, 'test@gmail.com')

		obj = f'{test_user.first_name}'
		self.assertEqual(obj, 'first')

		obj = f'{test_user.last_name}'
		self.assertEqual(obj, 'last')

	def test_account_labels(self):
		print('\nTesting account labels:')
		test_account = Account.objects.get(account_id=1)

		label = test_account._meta.get_field('account_id').verbose_name
		self.assertEqual(label, 'account id')

		label = test_account._meta.get_field('user').verbose_name
		self.assertEqual(label, 'user')

		label = test_account._meta.get_field('profile_picture').verbose_name
		self.assertEqual(label, 'profile picture')

		label = test_account._meta.get_field('date_created').verbose_name
		self.assertEqual(label, 'date created')

		label = test_account._meta.get_field('about_me').verbose_name
		self.assertEqual(label, 'about me')

	def test_account_values(self):
		print('\nTesting account values:')
		test_account = Account.objects.get(account_id=1)

		obj = f'{test_account.account_id}'
		self.assertEqual(obj, '1')

		obj = f'{test_account.user.id}'
		self.assertEqual(obj, '1')

		obj = f'{test_account.profile_picture}'
		self.assertEqual(obj, '')

		obj = f'{test_account.date_created}'
		self.assertTrue(obj)

		obj = f'{test_account.about_me}'
		self.assertEqual(obj, 'About me information')

	def test_post_labels(self):
		print('\nTesting post labels:')
		test_post = Post.objects.get(post_id=1)

		label = test_post._meta.get_field('post_id').verbose_name
		self.assertEqual(label, 'post id')

		label = test_post._meta.get_field('symbol').verbose_name
		self.assertEqual(label, 'symbol')

		label = test_post._meta.get_field('post_title').verbose_name
		self.assertEqual(label, 'post title')

		label = test_post._meta.get_field('post_text').verbose_name
		self.assertEqual(label, 'post text')

		label = test_post._meta.get_field('post_date_created').verbose_name
		self.assertEqual(label, 'post date created')

		label = test_post._meta.get_field('user').verbose_name
		self.assertEqual(label, 'user')

	def test_post_values(self):
		print('\nTesting post values:')
		test_post = Post.objects.get(post_id=1)

		obj = f'{test_post.post_id}'
		self.assertEqual(obj, '1')

		obj = f'{test_post.symbol}'
		self.assertEqual(obj, 'RMTD')

		obj = f'{test_post.post_title}'
		self.assertEqual(obj, 'Title')

		obj = f'{test_post.post_text}'
		self.assertEqual(obj, 'Post text')

		obj = f'{test_post.post_date_created}'
		self.assertTrue(obj)

		obj = f'{test_post.user.id}'
		self.assertEqual(obj, '1')

	def test_rating_labels(self):
		print('\nTesting rating labels:')
		test_rating = Rating.objects.get(vote='UPVOTE')

		label = test_rating._meta.get_field('post').verbose_name
		self.assertEqual(label, 'post')

		label = test_rating._meta.get_field('user').verbose_name
		self.assertEqual(label, 'user')

		label = test_rating._meta.get_field('vote').verbose_name
		self.assertEqual(label, 'vote')

	def test_rating_values(self):
		print('\nTesting rating values:')
		test_rating = Rating.objects.get(vote='UPVOTE')

		obj = f'{test_rating.post.post_id}'
		self.assertEqual(obj, '1')

		obj = f'{test_rating.user.account_id}'
		self.assertEqual(obj, '1')

		obj = f'{test_rating.vote}'
		self.assertEqual(obj, 'UPVOTE')

	def test_comment_labels(self):
		print('\nTesting comment labels:')
		test_comment = Comment.objects.get(post_id=1)

		label = test_comment._meta.get_field('post_id').verbose_name
		self.assertEqual(label, 'post id')

		label = test_comment._meta.get_field('user').verbose_name
		self.assertEqual(label, 'user')

		label = test_comment._meta.get_field('comment').verbose_name
		self.assertEqual(label, 'comment')

		label = test_comment._meta.get_field('comment_date_created').verbose_name
		self.assertEqual(label, 'comment date created')

	def test_comment_values(self):
		print('\nTesting comment values:')
		test_comment = Comment.objects.get(post_id=1)

		obj = f'{test_comment.post_id}'
		self.assertEqual(obj, '1 | testuser POSTED ---> "Title"')

		obj = f'{test_comment.user.id}'
		self.assertEqual(obj, '1')

		obj = f'{test_comment.comment}'
		self.assertEqual(obj, 'This is a test comment')

		obj = f'{test_comment.comment_date_created}'
		self.assertTrue(obj)

'''
Class that tests the validity of Luna's forms.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class FormsTestCase(TestCase):
	def test_createuserform(self):
		print('\nTesting create user form:')
		data = {'username': 'createuser',
				'first_name': 'third',
				'last_name': 'fourth',
				'email': 'testmail@gmail.com',
				'password1': 'valid1234',
				'password2': 'valid1234'
		}
		form = CreateUserForm(data=data)
		self.assertTrue(form.is_valid())

	def test_createuserform_invalid(self):
		print('\nTesting create user form (weak password):')
		data = {'username': 'createuser',
				'first_name': 'third',
				'last_name': 'fourth',
				'email': 'testmail@gmail.com',
				'password1': 'weak',
				'password2': 'weak'
		}
		form = CreateUserForm(data=data)
		self.assertFalse(form.is_valid())

	def test_createpostform(self):
		print('\nTesting create post form:')
		data = {'post_title': 'Create', 
				'symbol': 'RMTD', 
				'post_text': 'Testing post creation'
		}
		form = CreatePost(data=data)
		self.assertTrue(form.is_valid())

	def test_createcommentform(self):
		print('\nTesting create comment form:')
		user = User.objects.create_user(
			username='testuser',
			email='test@gmail.com',
			first_name='first',
			last_name='last',
			password='testingpass1'
		)

		post = Post.objects.create(
			post_id = 1,
			symbol='RMTD',
			post_title='Title',
			post_text='Post text',
			post_date_created=None,
			user=User.objects.get(id=1)
		)

		data = {'post_id': post.post_id,
				'user': user,
				'comment': 'This is a comment for tests'
		}
		form = CreateComment(data=data)
		self.assertTrue(form.is_valid())

'''
Class that tests HTTP responses for Luna's webpages.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class ViewsTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(
			username='testuser',
			email='test@gmail.com',
			first_name='first',
			last_name='last',
			password='testingpass1'
		)

		Account.objects.create(
			account_id=User.objects.get(id=1).id,
			user=User.objects.get(id=1),
			profile_picture=None,
			date_created=None,
			about_me='About me information'
		)

		Post.objects.create(
			post_id = 1,
			symbol='RMTD',
			post_title='Title',
			post_text='Post text',
			post_date_created=None,
			user=User.objects.get(id=1)
		)

		Rating.objects.create(
			post=Post.objects.get(post_id=1),
			user=Account.objects.get(account_id=1),
			vote='UPVOTE'
		)

		Comment.objects.create(
			post_id=Post.objects.get(post_id=1),
			user=User.objects.get(id=1),
			comment='This is a test comment',
			comment_date_created=None
		)

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.get(id=1)
		self.client = Client()

	# home
	def test_view_home(self):
		print('\nTesting view home:')
		request = self.factory.get('/luna')
		request.user = self.user
		response = home(request)
		self.assertEqual(response.status_code, 200)

	def test_view_home_anonymous(self):
		print('\nTesting view home with anonymous user:')
		request = self.factory.get('/luna')
		request.user = AnonymousUser()
		response = home(request)
		self.assertEqual(response.status_code, 200)
	
	# profile	
	def test_view_profile(self):
		print('\nTesting view profile:')
		request = self.factory.get('/luna/p/')
		request.user = self.user
		response = profile(request)
		self.assertEqual(response.status_code, 200)

	def test_view_profile_anonymous(self):
		print('\nTesting view profile with anonymous user:')
		request = self.factory.get('/luna/p/')
		request.user = AnonymousUser()
		response = profile(request)
		self.assertEqual(response.status_code, 302)
		response.client = self.client
		self.assertRedirects(response, '/li/?next=/luna/p/')

	# profile settings
	def test_view_profile_settings(self):
		print('\nTesting view profile settings:')
		request = self.factory.get('/luna/ps/')
		request.user = self.user
		response = profilesettings(request)
		self.assertEqual(response.status_code, 200)

	def test_view_profile_settings_anonymous(self):
		print('\nTesting view profile settings with anonymous user:')
		request = self.factory.get('/luna/ps/')
		request.user = AnonymousUser()
		response = profilesettings(request)
		self.assertEqual(response.status_code, 302)
		response.client = self.client
		self.assertRedirects(response, '/li/?next=/luna/ps/')

	#login
	def test_view_login(self):
		print('\nTesting view login:')
		request = self.factory.get('/luna/li/')
		request.user = self.user
		response = login_page(request)
		self.assertEqual(response.status_code, 302)
		response.client = self.client
		self.assertRedirects(response, '/')

	def test_view_login_anonymous(self):
		print('\nTesting view login with anonymous user:')
		request = self.factory.get('/luna/li/')
		request.user = AnonymousUser()
		response = login_page(request)
		self.assertEqual(response.status_code, 200)

	# sign up
	def test_view_sign_up(self):
		print('\nTesting view sign up:')
		request = self.factory.get('/luna/su/')
		request.user = self.user
		response = signup(request)
		self.assertEqual(response.status_code, 302)
		response.client = self.client
		self.assertRedirects(response, '/')

	def test_view_sign_up_anonymous(self):
		print('\nTesting view sign up with anonymous user:')
		request = self.factory.get('/luna/su/')
		request.user = AnonymousUser()
		response = signup(request)
		self.assertEqual(response.status_code, 200)

	# stock
	def test_view_stock(self):
		print('\nTesting view stock:')
		request = self.factory.get('/luna/stock/')
		request.user = self.user
		response = stock(request)
		self.assertEqual(response.status_code, 200)

	def test_view_stock_anonymous(self):
		print('\nTesting view stock with anonymous user:')
		request = self.factory.get('/luna/stock/')
		request.user = AnonymousUser()
		response = stock(request)
		self.assertEqual(response.status_code, 200)

	# new post
	def test_view_new_post(self):
		print('\nTesting view new post:')
		request = self.factory.get('/luna/np/')
		request.user = self.user
		response = newpost(request)
		self.assertEqual(response.status_code, 200)

	def test_view_new_post_anonymous(self):
		print('\nTesting view new post with anonymous user:')
		request = self.factory.get('/luna/np/')
		request.user = AnonymousUser()
		response = newpost(request)
		self.assertEqual(response.status_code, 302)
		response.client = self.client
		self.assertRedirects(response, '/li/?next=/luna/np/')

	# view post
	def test_view_view_post(self):
		print('\nTesting view view post:')
		request = self.factory.get('/luna/vp/1')
		request.user = self.user
		response = viewpost(request)
		self.assertEqual(response.status_code, 200)

	def test_view_view_post_anonymous(self):
		print('\nTesting view view post with anonymous user:')
		request = self.factory.get('/luna/vp/1')
		request.user = AnonymousUser()
		response = viewpost(request)
		self.assertEqual(response.status_code, 302)
		response.client = self.client
		self.assertRedirects(response, '/li/?next=/luna/vp/1')

'''
Class that tests view functions that require a form.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class ViewsIntegrationTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(
			username='testuser',
			email='test@gmail.com',
			first_name='first',
			last_name='last',
			password='testingpass1'
		)

		Account.objects.create(
			account_id=User.objects.get(id=1).id,
			user=User.objects.get(id=1),
			profile_picture=None,
			date_created=None,
			about_me='About me information'
		)

		Post.objects.create(
			post_id = 1,
			symbol='RMTD',
			post_title='Title',
			post_text='Post text',
			post_date_created=None,
			user=User.objects.get(id=1)
		)

		Rating.objects.create(
			post=Post.objects.get(post_id=1),
			user=Account.objects.get(account_id=1),
			vote='UPVOTE'
		)

		Comment.objects.create(
			post_id=Post.objects.get(post_id=1),
			user=User.objects.get(id=1),
			comment='This is a test comment',
			comment_date_created=None
		)

		Group.objects.create(
			name='access'
		)

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.get(id=1)
		self.client = Client()

	def test_login(self):
		print('\nTesting logging in:')
		request = self.factory.post(
			'/luna/li/',
			data={'fname': 'testuser',
				'psswd': 'testingpass1'}
		)
		request.user = AnonymousUser()
		setattr(request, 'session', self.client.session)
		#request.session = self.client.session
		request.session['key'] = 'value'

		response = login_page(request)
		response.client = self.client
		self.assertEqual(response.status_code, 302)

	def test_login_invalid(self):
		print('\nTesting logging in (user does not exist):')
		request = self.factory.post(
			'/luna/li/',
			data={'fname': 'notauser',
				'psswd': 'failing1234'}
		)
		request.user = AnonymousUser()
		setattr(request, 'session', self.client.session)
		#request.session = self.client.session
		request.session['key'] = 'value'

		response = login_page(request)
		response.client = self.client
		self.assertEqual(response.status_code, 200)

	def test_sign_up_creation(self):
		print('\nTesting creating a new user')
		request = self.factory.post(
			'/luna/su/',
			data={'username': 'createuser',
				'first_name': 'third',
				'last_name': 'fourth',
				'email': 'testmail@gmail.com',
				'password1': 'valid1234',
				'password2': 'valid1234'
			}
		)
		request.user = AnonymousUser()

		setattr(request, 'session', 'session')
		messages = FallbackStorage(request)
		setattr(request, '_messages', messages)

		response = signup(request)
		response.client = self.client
		self.assertRedirects(response, '/li/')

	def test_new_post_creation(self):
		print('\nTesting creating a new post')
		
		request = self.factory.post(
			'/luna/np/', 
			data={'post_title': 'Create', 
				'symbol': 'RMTD', 
				'post_text': 'Testing post creation'
			}
		)
		request.user = self.user

		response = newpost(request)
		response.client = self.client
		self.assertEqual(response.status_code, 200)

'''
Class that tests helper functions in views.py.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class ViewsHelperTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		User.objects.create_user(
			username='testuser',
			email='test@gmail.com',
			first_name='first',
			last_name='last',
			password='testingpass1'
		)

		Account.objects.create(
			account_id=User.objects.get(id=1).id,
			user=User.objects.get(id=1),
			profile_picture=None,
			date_created=None,
			about_me='About me information'
		)

		Post.objects.create(
			post_id = 1,
			symbol='RMTD',
			post_title='Title',
			post_text='Post text',
			post_date_created=None,
			user=User.objects.get(id=1)
		)

		Rating.objects.create(
			post=Post.objects.get(post_id=1),
			user=Account.objects.get(account_id=1),
			vote='UPVOTE'
		)

		Comment.objects.create(
			post_id=Post.objects.get(post_id=1),
			user=User.objects.get(id=1),
			comment='This is a test comment',
			comment_date_created=None
		)

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.get(id=1)
		self.client = Client()

	def test_createVote(self):
		print('\nTesting vote creation:')
		request = self.factory.get('/luna/')
		request.user = self.user
		post = Post.objects.create(
			post_id = 2,
			symbol='TSLA',
			post_title='Invalid',
			post_text='Dummy text for test',
			post_date_created=None,
			user=self.user
		)
		user = Account.objects.get(account_id=1)

		response = createVote(request, post.post_id, user.account_id, 'UPVOTE')
		response.client = self.client
		self.assertEqual(response.status_code, 302)

		vote = Rating.objects.get(post=post)
		self.assertEqual(vote.vote, 'UPVOTE')

	def test_createVote_overwrite(self):
		print('\nTesting vote creation (rating exists):')
		request = self.factory.get('/luna/')
		request.user = self.user
		post = Post.objects.get(post_id=1)
		user = Account.objects.get(account_id=1)

		response = createVote(request, post.post_id, user.account_id, 'DOWNVOTE')
		response.client = self.client
		self.assertEqual(response.status_code, 302)

		vote = Rating.objects.get(post=post)
		self.assertEqual(vote.vote, 'DOWNVOTE')

	def test_findVote(self):
		print('\nTesting find vote:')
		request = self.factory.get('/luna/')
		request.user = self.user
		post = Post.objects.get(post_id=1)

		response = findVote(request, 1)
		self.assertEqual(response, 'UPVOTE')

	def test_findVote_invalid(self):
		print('\nTesting find vote (vote does not exist):')
		request = self.factory.get('/luna/')
		request.user = self.user
		Post.objects.create(
			post_id = 2,
			symbol='TSLA',
			post_title='Invalid',
			post_text='Dummy text for test',
			post_date_created=None,
			user=self.user
		)

		response = findVote(request, 2)
		self.assertEqual(response, 'NONE')
