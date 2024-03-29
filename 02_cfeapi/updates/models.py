from django.core.serializers import serialize
from django.db import models
import json
from django.conf import settings

# Create your models here.
def upload_to_image(instance, filename):
    return "updates/{user}/{filename}/".format(user=instance.user, filename=filename)


class UpdateQuerySet(models.QuerySet):
    # def serialize(self):
    #     qs = self
    #     return serialize("json", qs, fields=('user', 'content', 'image'))

    # def serialize(self):
    #     qs = self
    #     final_array = []
    #     for obj in qs:
    #         stuct = json.loads(obj.serialize())
    #         final_array.append(stuct)
    #     return json.dumps(final_array)

    def serialize(self):
        list_values = list(self.values("user", "content", "image"))
        return json.dumps(list_values)


class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model, using=self._db)


class Update(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content     = models.TextField(blank=True, null=True)
    image       = models.ImageField(upload_to=upload_to_image, blank=True, null=True)
    updated     = models.DateField(auto_now=True)
    timestamp   = models.DateField(auto_now_add=True)

    objects = UpdateManager()

    def __str__(self) -> str:
        return self.content or ""

    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ""

        data = {
            "user": self.user,
            "image": image,
            "content": self.content
        }
        data = json.dumps(data)
        return data