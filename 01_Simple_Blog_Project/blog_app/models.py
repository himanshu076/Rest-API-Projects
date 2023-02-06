from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=130)
    # description = models.TextField(default="")
    # image = models.ImageField(upload_to='post', null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    upvote_count = models.IntegerField(default=0)
    # post_status = models.IntegerField(choices=STATUS, default=0)
    # related_posts = models.ManyToManyField('Post', blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Upvote(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), related_name = 'upvotes',
                                                                on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"), related_name = 'upvotes',
                                                                on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body