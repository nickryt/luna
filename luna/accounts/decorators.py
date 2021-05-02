from django.http import HttpResponse
from django.shortcuts import redirect

'''
Determines user authentication and authorization when accessing a view function.

IF A VIEW IN VIEWS.PY HAS THIS DECORATOR OVER IT, THIS MEANS THAT
ONLY AN UNAUTHENTICATED USER CAN VIEW THE PAGE (FOR EXAMPLE, LOG IN OR SIGN UP PAGES)

THE VIEW IS REDIRECTED TO THE HOME PAGE IF A USER IS ALREADY LOGGED IN

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''

'''
Determines if the user is registered in Luna's database.

@param function in views.py
@return Redirect to home page if unauthenticated, else runs the given view function
'''
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('homepage')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func

'''
Determines if the user has authorization to view page.
Used to differenciate between admin and registered user.

@param list of groups that can access the function
@return Runs the given view function, else returns an HTTP response if user is not authorized
'''
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page.')
		return wrapper_func
	return decorator