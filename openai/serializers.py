from rest_framework.serializers import ModelSerializer

from openai.models import Art


class ArtSerializer(ModelSerializer):
    class Meta:
        model = Art
        fields = ('id', 'description', 'image', 'user')