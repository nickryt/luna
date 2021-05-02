from django.db import models
from django.contrib.auth.models import User

'''
Class that defines the Account database model.
Account model is linked to user model.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='img', default='img/moolah.png', null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    about_me = models.CharField(max_length=10000, default="About Me", null=True)

    def __str__(self):
        if self.user:
            return str(self.user.username)
        else:
            return 'ERROR'

'''
Class that defines the Post database model.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)  
    symbol = models.CharField(max_length=5, null=True)
    post_title = models.CharField(max_length=250, null=True)
    post_text = models.CharField(max_length=10000, null=True)
    post_date_created = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.post_id) + " | " + str(self.user) + " POSTED ---> \"" + self.post_title + "\""

'''
Class that defines the Rating database model.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class Rating(models.Model):
    VOTING_CHOICES = (('DOWNVOTE', 'DOWNVOTE'), ('UPVOTE', 'UPVOTE'))
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    vote = models.CharField(max_length=50, null=True, choices=VOTING_CHOICES)

    def __str__(self):
        return str(self.vote) + " By " + str(self.user.user) + " On " + str(self.post)

'''
Class that defines the Comment database model.

@author Christopher Clemente, Liman Chang, Nicholas Rytelewski, Zabir Rahman
'''
class Comment(models.Model):
    post_id = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=10000, null=False)
    comment_date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user) + " ---> \"" + self.comment + "\""
