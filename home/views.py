from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
from wagtail.core.models import Page
from wagtail.images.models import Image
from rest_framework import generics
from .serializers import BlogCategorySerializer, BlogAuthorSerializer
from .models import (
    BlogPage,
    BlogCategory,
    HomePage,
    BlogAuthor,
    BlogMetaTags,
    BlogTags,
)

class BlogPagesApiView(generics.GenericAPIView):
    def list(self, request, *args, **kwargs):


        query_expr = Q()
        query_expr &= Q(title__icontains=self.request.GET.get('search')) | \
        Q(blog_content__icontains=self.request.GET.get('search')) \
        if self.request.GET.get('search') else Q()
        query_expr &= Q(tags__tags__name__in=self.request.GET.get(
            'tags').split(',')) if self.request.GET.get('tags',0) \
            else Q()
        query_expr &= Q(meta_tags__meta_tags__name__in=self.request.GET.get(
            'meta_tags').split(',')) if self.request.GET.get('meta_tags', 0) \
            else Q()
        query_expr &= Q(blog_categories__slug=self.request.GET.get('category_slug')) \
            if self.request.GET.get('category_slug', 0) \
            else Q()
        queryset = BlogPage.objects.live().public().filter(query_expr)
        results = []
        for page in queryset:
            parent = page.get_parent().specific
            results.append({
                'id': page.id,
                'parent_title':parent.title,
                'title': page.title,
                'slug': page.slug,
                'seo_title': page.seo_title,
                'search_description': page.search_description,
                'blog_date': page.blog_date,
                'blog_categories': [
                    {'name': category.name,
                     'slug': category.slug,
                     'icon': category.icon.file.url}
                    for category in page.blog_categories.all()
                ],
                'blog_likes': page.blog_likes,
                'blog_is_hot': page.blog_is_hot,
                'blog_content': page.blog_content,
                'blog_image': page.blog_image.file.url,
                'tags': [
                    {'name': PostPageBlogTags.tags.name}
                    for PostPageBlogTags in page.tags.all()
                ],
                'meta_tags': [
                    {'name': PostPageBlogMetaTags.meta_tags.name}
                    for PostPageBlogMetaTags in page.meta_tags.all()
                ],
                'blog_author': [
                    {
                        'author': BlogAuthorsOrderable.author.name,
                        'image':
                            BlogAuthorsOrderable.author.get_image_thumbnail(),
                    }
                    for BlogAuthorsOrderable in page.blog_authors.all()

                ]
            })

        return Response(results)

    def retrieve(self, request, slug=None, *args, **kwargs):
        page = get_object_or_404(BlogPage, slug=slug)
        parent = page.get_parent().specific
        result = {
            'id': page.id,
            'parent_title': parent.title,
            'title': page.title,
            'slug': page.slug,
            'seo_title': page.seo_title,
            'search_description': page.search_description,
            'blog_date': page.blog_date,
            'blog_categories': [
                {'name': category.name,
                 'slug': category.slug,
                 'icon': category.icon.file.url}
                for category in page.blog_categories.all()
            ],
            'blog_likes': page.blog_likes,
            'blog_is_hot': page.blog_is_hot,
            'blog_content': page.blog_content,
            'blog_image': page.blog_image.file.url,
            'tags': [
                {'name': PostPageBlogTags.tags.name}
                for PostPageBlogTags in page.tags.all()
            ],
            'meta_tags': [
                {'name': PostPageBlogMetaTags.meta_tags.name}
                for PostPageBlogMetaTags in page.meta_tags.all()
            ],
            'blog_author': [
                {
                    'author': BlogAuthorsOrderable.author.name,
                    'image': BlogAuthorsOrderable.author.get_image_thumbnail(),
                }
                for BlogAuthorsOrderable in page.blog_authors.all()
            ]
        }

        return Response(result)
    def get_queryset(self):
        return BlogPage.objects.live().public()
    def get(self, request, *args, **kwargs):
        if 'slug' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)





class BlogCategoryListCreateView(generics.ListCreateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer

class BlogAuthorListCreateView(generics.ListCreateAPIView):
    queryset = BlogAuthor.objects.all()
    serializer_class = BlogAuthorSerializer

class HomePageApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = HomePage.objects.live().public()
        results = []
        for page in queryset:
            results.append({
                'id': page.id,
                'title': page.title,
                'slug': page.slug,
                'banner_image': page.banner_image.file.url,
                'search_description': page.search_description,
            })

        return Response(results)

    def get_queryset(self):
        return HomePage.objects.live().public()


class BlogsTagsApiView(APIView):
    def get(self, request, *args, **kwargs):
        queryset_tags = BlogTags.objects.all()
        queryset_meta_tags = BlogMetaTags.objects.all()
        tags_list = []
        meta_tags_list = []
        results = {}
        for tags in queryset_tags:
            tags_list.append({
                'name': tags.name,
            })
        for meta_tags in queryset_meta_tags:
            meta_tags_list.append({
                'name': meta_tags.name,
            })
        results['tags'] = tags_list
        results['meta_tags'] = meta_tags_list
        print("RESULT", results)
        return Response(results)

