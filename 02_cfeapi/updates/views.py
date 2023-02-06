from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
import json
from django.core.serializers import serialize

from updates.models import Update
from cfeapi.mixins import JsonResponseMixin

# Create your views here.
# def detail_view(request):
    # return render() # return JSON Data XML  --> JS Object Notion

# obj = Update.objects.get(id=1)

def update_model_detail_view(request):
    """
    URI -- for Rest API
    """
    data = {
        "count" : 1000,
        "content": "Some New content"
    }
    return JsonResponse(data)

# *Conterting above function into Class Based View
class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        data = {
            "count" : 1000,
            "content": "Some New content"
        }
        return JsonResponse(data)


class JsonCBV2(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "count" : 1000,
            "content": "Some New content"
        }


class SerializedView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=1)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        qs = Update.objects.all()
        json_data = qs.serialize()
        return HttpResponse(json_data, content_type='application/json')