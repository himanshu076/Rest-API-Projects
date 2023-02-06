from django.conf import settings
from django.db import models

# Create your models here.
def upload_status_image(instance, filename):
    return "status/{user}/{filename}".format(user=instance.user, filename=filename)


class StatusQueryset(models.QuerySet):
    pass


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQueryset(self.model, using=self._db)

class Status(models.Model): #fb status, instagram post, tweet, linkedin post
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # User Instance .save()
    content     = models.TextField(null=True, blank=True)
    image       = models.ImageField(upload_to=upload_status_image, null=True, blank=True)
    updated     = models.DateField(auto_now=True)
    timestamp   = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.content)[:50]

    class Meta:
        verbose_name = "Status Post"
        verbose_name_plural = "Status Posts"


