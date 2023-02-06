from io import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from status.api.serializers import StatusSerializer
from status.models import Status

"""
Serialize a single object
"""
obj = Status.objects.first()
serializer = StatusSerializer(obj)
serializer.data
json_data = JSONRenderer().render(serializer.data)
print(json_data)

stream = BytesIO(json_data)
data = JSONParser.parse(stream)
print(data)


'''
Serialize a queryset
'''
qs = Status.objects.all()
serializer2 = StatusSerializer(qs, many=True)
print(serializer2.data)
json_data2 = JSONRenderer().render(serializer2.data)
print(json_data2)

stream2 = BytesIO(json_data2)
data2 = JSONParser().parse(stream2)
print(data2)


'''
Create Object
'''
data = {"user": 1}
serializer = StatusSerializer(data=data)
serializer.is_valid()
serializer.save()

# if serializer.is_valid():
#     serializer.save()

'''
Update Object
'''
obj = Status.objects.first()
data = {'user': 1, 'content': "Some new new content"}
serializer = StatusSerializer(obj, data=data)
serializer.is_valid()
serializer.save()


'''
Delete Object
'''
obj = Status.objects.first()
data = {'user': 1, 'content': "Please Delete Me."}
Create_obj_serializer = StatusSerializer(data=data)
Create_obj_serializer.is_valid()
Create_obj = Create_obj_serializer.save() # return instance of the object
print(Create_obj)


# data = {'id': 3}
obj = Status.objects.last()
get_data_serializer = StatusSerializer(obj)
print(get_data_serializer.data)
# update_serializer.is_valid()
# update_serializer.save()