from wagtail.api.v2.serializers import PageSerializer
from rest_framework import serializers
from home.models import BlogPage, BlogCategory, BlogAuthor

class BlogPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPage
        fields = '__all__'

class BlogCategorySerializer(serializers.ModelSerializer):
    icon = serializers.ReadOnlyField(source='get_icon_thumbnail')
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'icon']


class BlogAuthorSerializer(serializers.ModelSerializer):

    image = serializers.ReadOnlyField(source='get_image_thumbnail')
    class Meta:
        model = BlogAuthor
        fields = '__all__'
