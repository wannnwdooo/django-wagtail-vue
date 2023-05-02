from wagtail.api.v2.views import PagesAPIViewSet
from home.models import BlogPage, BlogCategory
from django_filters import rest_framework as filters
from rest_framework import serializers
from .filters import BlogCategorySlugFilter

class BlogPageFilter(filters.FilterSet):
    blog_content = filters.CharFilter(lookup_expr='icontains')
    blog_categories = BlogCategorySlugFilter()

    class Meta:
        model = BlogPage
        fields = ['blog_title', 'blog_categories']


class BlogPagesAPIViewSet(PagesAPIViewSet):
    filter_backends = PagesAPIViewSet.filter_backends + [filters.DjangoFilterBackend]
    filterset_class = BlogPageFilter

    known_query_parameters = PagesAPIViewSet.known_query_parameters.union({"blog_content", "blog_categories"})

    def get_queryset(self):
        return BlogPage.objects.all().live()