from django.db import models
from django import forms
from django.utils.text import slugify
from transliterate import translit
from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework import serializers
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.search import index
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel as \
    DefaultImageChooserPanel
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField
from home import blocks
from django.db import models
from django import forms
from django.shortcuts import render
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
class TextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock()


class ImageChooserPanel(DefaultImageChooserPanel):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                'id': value.id,
                'title': value.title,
                'large': value.get_rendition('width-1000').attrs_dict,
                'thumbnail': value.get_rendition('fill-120x120').attrs_dict,
            }



class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                'id': value.id,
                'title': value.title,
                'large': value.get_rendition('width-1000').attrs_dict,
                'thumbnail': value.get_rendition('fill-120x120').attrs_dict,
            }

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True,
                            blank=True)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('icon'),
    ]

    api_fields = [
        APIField('name'),
        APIField('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name, reversed=True))
        super().save(*args, **kwargs)

    def get_icon_thumbnail(self):
        if self.icon:
            thumbnail = self.icon.get_rendition('fill-80x80')
            return thumbnail.url
        else:
            return None


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("home.BlogPage", related_name="blog_authors")
    author = models.ForeignKey(
        "home.BlogAuthor",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("page", "author")



    panels = [
        SnippetChooserPanel("author"),
    ]

    def __str__(self):
        return self.author.name
@register_snippet
class BlogTags(models.Model):
    name = models.CharField(max_length=255, unique=True)

    panels = [
        FieldPanel("name"),
    ]
    api_fields = [
        APIField('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

@register_snippet
class BlogMetaTags(models.Model):
    name = models.CharField(max_length=255, unique=True)

    panels = [
        FieldPanel("name"),
    ]
    api_fields = [
        APIField('name'),
    ]
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Meta Tag"
        verbose_name_plural = "Meta Tags"


@register_snippet
class BlogAuthor(models.Model):
    """Blog author for snippets."""

    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]

    def get_image_thumbnail(self):
        if self.image:
            thumbnail = self.image.get_rendition('fill-120x120')
            return thumbnail.url
        else:
            return None

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

class BlogCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = ['name', 'slug', 'icon']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        blog_category = BlogCategory.objects.filter(icon=ret['icon']).first()
        ret['icon'] = blog_category.get_icon_thumbnail()
        return ret

class BlogAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogAuthorsOrderable
        fields = ['id',]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        orderable = BlogAuthorsOrderable.objects.filter(id=ret['id']).first()
        author = BlogAuthor.objects.get(id=orderable.author.id)
        image = author.get_image_thumbnail()
        ret['author'] = author.name
        ret['image'] = image
        return ret

class PostPageBlogTags(models.Model):
    page = ParentalKey(
        "home.BlogPage", on_delete=models.CASCADE, related_name="tags"
    )
    tags = models.ForeignKey(
        "home.BlogTags", on_delete=models.CASCADE, related_name="pages"
    )

    panels = [
        SnippetChooserPanel("tags"),
    ]
    def __str__(self):
        return self.tags.name

class PostPageBlogMetaTags(models.Model):
    page = ParentalKey(
        "home.BlogPage", on_delete=models.CASCADE, related_name="meta_tags"
    )
    meta_tags = models.ForeignKey(
        "home.BlogMetaTags", on_delete=models.CASCADE, related_name="pages")

    panels = [
        SnippetChooserPanel("meta_tags"),
    ]

    def __str__(self):
        return self.meta_tags.name

class BlogPage(Page):
    """Blog detail page."""
    template = "home/blog_page.html"
    blog_date = models.DateField("Post date")
    blog_categories = ParentalManyToManyField('home.BlogCategory', blank=True)
    blog_is_hot = models.BooleanField(default=False)
    blog_likes = models.IntegerField(default=0)

    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    blog_content = RichTextField("Контент для блога")


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("blog_content"),
            FieldPanel("blog_date"),
            FieldPanel('blog_categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel("blog_is_hot", widget=forms.CheckboxInput),
            FieldPanel("blog_likes"),
        ], heading="Blog information"),
        InlinePanel("tags", label="tags", min_num=0),
        InlinePanel("meta_tags", label="meta_tags", min_num=0),
        ImageChooserPanel("blog_image"),
        InlinePanel("blog_authors", label="Author", min_num=1, max_num=1),
    ]
    api_fields = [
            APIField('blog_date'),
            APIField('live'),
            APIField('blog_likes'),
            APIField(
                'blog_categories',
                serializer=BlogCategoriesSerializer(many=True)
            ),
            APIField('blog_is_hot'),
            APIField('blog_content'),
            APIField('blog_image'),
            APIField('tags', serializer=serializers.StringRelatedField(many=True)
                     ),
            APIField('meta_tags', serializer=serializers.StringRelatedField(many=True)
                     ),
            APIField('blog_authors', serializer=BlogAuthorSerializer(many=True)),
        ]

    search_fields = Page.search_fields + [
        index.SearchField('blog_content'),
    ]

class HomePage(Page):
    template = "home/home_page.html"

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("banner_image"),
    ]

    api_fields = [
        APIField('banner_image'),
    ]

    def save(self, *args, **kwargs):
        if self.pk is None and HomePage.objects.exists():
            raise ValidationError('Главная страница может быть только одна!')
        return super().save(*args, **kwargs)

