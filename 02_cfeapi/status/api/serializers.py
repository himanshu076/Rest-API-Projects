from rest_framework import serializers

from status.models import Status

'''
Serializers -> JSON
Serializers -> Validate Data

class CustomSerializer(serializers.Serializer):
    content     = serializers.CharField()
    email       = serializers.EmailField()
'''

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'id',
            'user',
            'content',
            'image',
        ]

        read_only_fields = ['user'] # GET

    # def valid_content(self, value):
    #     if len(value) > 10000:
    #         raise serializers.ValidationError("This is way too long.")
    #     return value

    def validate(self, data):
        content = data.get('content', None)
        if content == "":
            content = None
        image = data.get('imgae', None)
        if content is None and image is None:
            raise serializers.ValidationError("Content or Imnage is required.")
        return data

