from django.contrib import admin
from .models import *

'''
Register models from model.py into the database.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(Comment)