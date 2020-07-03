from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedModelSerializer(label='地址', read_only=True, view_name='user-detail', lookup_field='id')

    class Meta:
        model = User
        fields = ['id',  'username', 'email', 'groups']
        # fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'user_set']
