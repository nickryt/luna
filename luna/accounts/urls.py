from django.urls import path
from . import views

'''
List of all url patterns used and their respective view function.
Exists to help page redirection in the functions.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
urlpatterns = [
    path('', views.home, name="homepage"),
    path('p/', views.profile, name="profile_page"),
    path('ps/', views.profilesettings, name="settings_page"),
    path('up/', views.updateprofile, name="update_profile"),
    path('dlt/', views.deleteprofile, name="delete_profile"),
    path('li/', views.login_page, name="login_page"),
    path('lo/', views.log_out, name="logout_funct"),
    path('su/', views.signup, name="signup_page"),
    path('stock/', views.stock, name="stock_page"),
    path('np/', views.newpost),
    path('vp/<str:post_key>', views.viewpost, name="view_post"),
    path('dp/<str:post_key>', views.deletepostredirect, name='delete_post'),
    path('dc/<str:comment_key>/<str:post_key>', views.deletecommentredirect, name='delete_comment'),
    path('v/<str:post_key>/<str:user_id>/<str:voted>', views.createVote, name='vote')
]
