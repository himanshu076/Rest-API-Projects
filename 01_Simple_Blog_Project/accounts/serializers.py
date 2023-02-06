from rest_framework import serializers

from accounts.models import User


class UserModelSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(min_length = 8, write_only = True)
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'last_login', 'first_name', 'last_name', 'username', 'email',
                    'phone_number', 'roll', 'is_active', 'date_joined', 'age', 'gender',
                    'profile_pic', 'bio', 'groups')
        extra_kwargs = {'password':{'write_only':True}}



