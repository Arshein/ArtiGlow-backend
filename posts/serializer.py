from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from posts.models import Post
from accounts.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'description', 'owner', 'image', 'created_at', 'updated_at',)
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        post_obj  = Post.objects.create(**validated_data)
        return post_obj