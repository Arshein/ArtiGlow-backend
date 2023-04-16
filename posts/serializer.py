import urllib

from django.conf import settings
from django.core.files import File
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from posts.models import Post
from accounts.serializers import UserSerializer
from .image_resource import gen_image

import requests, uuid, os
from django.core.files.temp import NamedTemporaryFile
class PostSerializer(ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'description', 'owner', 'image', 'created_at', 'updated_at',)
        read_only_fields = ['id', 'created_at', 'image', 'updated_at']

    def create(self, validated_data):
        # set post owner
        validated_data['owner'] = self.context['request'].user

        # generate image from prompt
        try:
            image_url = gen_image(validated_data['description'])
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred while generating the image: {e}")

        # download and save image temporarily
        r = requests.get(image_url)
        if r.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(r.content)
            img_temp.flush()
        else:
            raise serializers.ValidationError(f"An error occurred while generating the image: could not download image at {image_url}")

        # save post with image
        post_obj = Post.objects.create(**validated_data)
        post_obj.image.save(os.path.basename(image_url) + '.jpg', File(img_temp), save=True)

        return post_obj