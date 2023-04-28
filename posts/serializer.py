import urllib

from django.conf import settings
from django.core.files import File
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from posts.models import Post, Comment, Like
from accounts.serializers import UserSerializer
from .image_resource import gen_image

import requests, uuid, os
from django.core.files.temp import NamedTemporaryFile


class UserShortField(serializers.RelatedField):
    def to_representation(self, value):
        return {'id': value.id, 'username': value.username}


class LikeSerializer(serializers.ModelSerializer):
    owner = UserShortField(many=False, read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'post', 'owner', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        like_obj = Like.objects.create(**validated_data)
        return like_obj


class PostSerializer(ModelSerializer):
    owner = UserShortField(many=False, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    def __init__(self, args, **kwargs):

        # Don't return emails when listing users

        if kwargs['context']['view'].action == 'list':
            del self.fields['likes']

        super().__init__(args, **kwargs)

    class Meta:
        model = Post
        fields = (
        'id', 'description', 'owner', 'likes', 'likes_count', 'comments_count', 'image', 'created_at', 'updated_at',)
        read_only_fields = ['id', 'created_at', 'likes', 'image', 'likes_count', 'comments_count', 'updated_at']

    def create(self, validated_data):
        # set post owner
        validated_data['owner'] = self.context['request'].user

        try:
            # generate image from prompt
            image_url = gen_image(validated_data['description'])

            # download and save image temporarily
            r = requests.get(image_url)
            if r.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(r.content)
                img_temp.flush()
            else:
                raise Exception(f'could not download image at {image_url}')

        except Exception as e:
            raise serializers.ValidationError(f"An error occurred while generating the image: {e}")

        # save post with image
        post_obj = Post.objects.create(**validated_data)
        post_obj.image.save(os.path.basename(image_url) + '.jpg', File(img_temp), save=True)

        return post_obj


class CommentSerializer(serializers.ModelSerializer):
    owner = UserShortField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'owner', 'description', 'created_at')
        read_only_fields = ('id', 'created_at', 'post', 'owner')

