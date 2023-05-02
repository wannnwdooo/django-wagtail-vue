from django_filters import rest_framework as filters
from django.db.models import Q
from .models import BlogCategory


class BlogCategorySlugFilter(filters.Filter):
    def filter(self, queryset, value):
        if not value:
            return queryset

        slugs = value.split(',')
        queries = [Q(blog_categories__slug=slug) for slug in slugs]

        query = queries.pop()
        for item in queries:
            query |= item

        return queryset.filter(query)