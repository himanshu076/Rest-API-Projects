from django.contrib import admin
from blog_app.models import Post, Upvote, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Upvote)
admin.site.register(Comment)