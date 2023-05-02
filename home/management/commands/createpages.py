import os
from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_wsgi_application()
from django.core.files import File
from wagtail.core import blocks
from wagtail.images.models import Image
from wagtail.core.models import Page, Site
from wagtail.core.blocks import RichTextBlock, StreamValue
from django.utils.text import slugify
from faker import Faker
from django.contrib.contenttypes.models import ContentType
from home.blocks import TextBlock
from home.models import (
    BlogCategory,
    BlogAuthor,
    BlogTags,
    BlogMetaTags,
    BlogPage,
    TextBlock,
    HomePage,
    BlogAuthorsOrderable,
    PostPageBlogTags,
    PostPageBlogMetaTags,
)


class Command(BaseCommand):
    help = "Load blog data into database with images"



    def handle(self, *args, **options):

        try:
            # Получаем объект Image по естественному ключу
            blog_image = Image.objects.get(title='Image 1')
        except Image.DoesNotExist:
            # Если объект не найден, создаем новый
            with open('media/images/1.jpg', 'rb') as f:
                content = File(f)
                blog_image = Image.objects.create(
                    title='Image 1',
                    file=content,
                )
            with open('media/images/2.jpg', 'rb') as f:
                content = File(f)
                blog_image2 = Image.objects.create(
                    title='Image 2',
                    file=content,
                )
        else:
            print('Изображение уже загружены!')

        main = Page.objects.filter(title="Welcome to your new Wagtail site!").first()
        if main:
            print(f"Удаляем стартовую страницу: {main}")
            main.delete()

        root = Page.get_first_root_node()
        home = HomePage.objects.all().first()
        if home:
            print(f"Главная страница уже создана: {home}")
        else:
            home_page_content = ContentType.objects.get_for_model(
                HomePage
            )
            home_page = HomePage(
                title="compas.pro",
                banner_image=blog_image,
                draft_title="compas.pro",
                slug="root",
                content_type=home_page_content,
                show_in_menus=True
            )

            root.add_child(instance=home_page)
            print(f"Стартовая страница создана: {home_page}")

        # create Site objects
        site = Site.objects.all().first()
        root_page = HomePage.objects.filter(title="compas.pro").first()
        if site is None and root_page:
            Site.objects.create(
                hostname="localhost",
                root_page=root_page,
                is_default_site=True,
                site_name="compas.pro",
                port=8000,
            )
            print(f"Сайт compas.pro создан")

        #create Category objects
        category = [
            'О нас',
            'Актуально',
            'Важно',
            'Интересно',
            'Спорно',
            'Регионы',
        ]
        category_insatnce = BlogCategory.objects.filter(name__in=category)
        if category_insatnce:
            print("Категории уже созданы!")
        else:
            for name in category:
                BlogCategory.objects.create(name=name, icon=blog_image2)

        # create Author objects
        authors = [
            'Author 1',
            'Author 2',
        ]
        authors_instance = BlogAuthor.objects.filter(name__in=authors)
        if authors_instance:
            print("Авторы уже созданы!")
        else:
            for name in authors:

                BlogAuthor.objects.create(
                    name=name,
                    website='http://www.example.com',
                    image=blog_image
                )

        # Create BlogTags objects
        tags = [
            'Tag 1',
            'Tag 2',
            'Tag 3',
            'Tag 4',
            'Tag 5',
            'Tag 6',
        ]
        tags_instance = BlogTags.objects.filter(name__in=tags)
        if tags_instance:
            print("Тэги уже созданы")
        else:
            for name in tags:
                BlogTags.objects.create(name=name)
        # Create BlogMetaTags objects
        meta_tags = [
            'Meta Tag 1',
            'Meta Tag 2',
            'Meta Tag 3',
            'Meta Tag 4',
            'Meta Tag 5',
            'Meta Tag 6',
        ]
        meta_tags_instance = BlogMetaTags.objects.filter(name__in=meta_tags)
        if meta_tags_instance:
            print("Мета Тэги уже созданы")
        else:
            for name in meta_tags:
                BlogMetaTags.objects.create(name=name)

        # Create BlogPage objects
        homepage_content_type = ContentType.objects.get_for_model(
             BlogPage
        )
        blog_author = BlogAuthor.objects.filter(name='Author 1').first()
        blog_author2 = BlogAuthor.objects.filter(name='Author 2').first()
        tag1 = BlogTags.objects.filter(name='Tag 1').first()
        tag2 = BlogTags.objects.filter(name='Tag 2').first()
        meta_tag1 = BlogMetaTags.objects.filter(name='Meta Tag 1').first()
        meta_tag2 = BlogMetaTags.objects.filter(name='Meta Tag 2').first()
        cat1 = BlogCategory.objects.filter(name='О нас').first()
        cat2 = BlogCategory.objects.filter(name='Актуально').first()
        parent_page = HomePage.objects.filter(title="compas.pro").first()
        blog_page1 = BlogPage.objects.filter(slug='BlogPage1').first()
        blog_page2 = BlogPage.objects.filter(slug='BlogPage2').first()
        blog_page3 = BlogPage.objects.filter(slug='BlogPage3').first()


        if blog_page1:
            print("Страница blog_page2 уже создана!")
        else:
            blog_page1 = BlogPage(
                title='Blog Page 1',
                blog_date='2022-01-01',
                slug='BlogPage1',
                blog_is_hot=True,
                show_in_menus=True,
                blog_likes=5,
                blog_image=blog_image,
                blog_content='<p data-block-key=\"6n8tk\">Welcome to my page '
                             'BLOG PAGE 1!</p><p data-block-key=\"fua79\"> '
                             'Welcome to my page BLOG PAGE 1!</p>'
                             '<p data-block-key=\"agd9l\">'
                             ' It this a fucking page for dev! </p>'
                             '<p data-block-key=\"1mhi2\">Yes! Yes! '
                             'For development! </p><p data-block-key=\"6vagd\">'
                             'The next page may be attachment with images: </p>'
                             '<p data-block-key=\"9bug1\"></p><embed '
                             'alt=\"Image 1\" embedtype=\"image\" '
                             'format=\"fullwidth\" id=\"1\"/>'
                             '<p data-block-key=\"fmqta\">'
                             'Just text for this is fucking page!</p>'
                             '<p data-block-key=\"ccuko\">&gt;.&lt;</p>',
                content_type=homepage_content_type,
            )
            parent_page.add_child(instance=blog_page1)
            blog_author_orderable = BlogAuthorsOrderable(author=blog_author,
                                                         page=blog_page1)
            blog_page1.blog_authors.add(blog_author_orderable)
            post_page_blog_tag = PostPageBlogTags(tags=tag1)
            blog_page1.tags.add(post_page_blog_tag)
            post_page_blog_meta_tag = PostPageBlogMetaTags(meta_tags=meta_tag1)
            blog_page1.meta_tags.add(post_page_blog_meta_tag)
            blog_page1.blog_categories.add(cat1)
            blog_page1.save()

        if blog_page2:
            print("Страница blog_page2 уже создана!")
        else:
            blog_page2 = BlogPage(
                title='Blog Page 2',
                blog_date='2023-04-15',
                slug='BlogPage2',
                blog_is_hot=False,
                show_in_menus=True,
                blog_likes=10,

                blog_image=blog_image2,
                blog_content='<h1>Welcome to my page BLOG PAGE 2!</h1>',
                content_type=homepage_content_type,
            )
            parent_page.add_child(instance=blog_page2)
            blog_author_orderable = BlogAuthorsOrderable(author=blog_author,
                                                         page=blog_page2)
            blog_page2.blog_authors.add(blog_author_orderable)
            post_page_blog_tag = PostPageBlogTags(tags=tag2)
            blog_page2.tags.add(post_page_blog_tag)
            post_page_blog_meta_tag = PostPageBlogMetaTags(meta_tags=meta_tag2)
            blog_page2.meta_tags.add(post_page_blog_meta_tag)
            blog_page2.blog_categories.add(cat2)
            blog_page2.save()

        if blog_page3:
            print("Страница blog_page3 уже создана!")
        else:
            blog_page3 = BlogPage(
                title='Blog Page 3',
                blog_date='2023-02-11',
                slug='BlogPage3',
                blog_is_hot=False,
                show_in_menus=True,
                blog_likes=3,
                blog_image=blog_image,
                blog_content='<p data-block-key=\"6y5th\">'
                             'Welcome to my page BLOG PAGE 3!</p>'
                             '<p data-block-key=\"d261n\">'
                             'TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT</p>'
                             '<p data-block-key=\"8mrnh\">'
                             'the image will be on the next line'
                             '</p><embed alt=\"Image 2\" embedtype=\"image\" '
                             'format=\"left\" id=\"2\"/><p data-block-key=\
                             "fptpb\">the end.</p><p data-block-key=\"duh3h\">'
                             '</p>',
                content_type=homepage_content_type,
            )

            parent_page.add_child(instance=blog_page3)
            blog_author_orderable = BlogAuthorsOrderable(author=blog_author,
                                                         page=blog_page3)
            blog_page3.blog_authors.add(blog_author_orderable)
            post_page_blog_tag = PostPageBlogTags(tags=tag1)
            blog_page3.tags.add(post_page_blog_tag)
            post_page_blog_meta_tag = PostPageBlogMetaTags(meta_tags=meta_tag1)
            blog_page3.meta_tags.add(post_page_blog_meta_tag)
            blog_page3.blog_categories.add(cat2)
            blog_page3.save()

        pages_count = Page.objects.all().count()
        if pages_count >= 100:
            print("Все страницы сгенерированы")
        else:
            fake = Faker()
            root_page = Page.objects.get(title='Root')
            author = BlogAuthor.objects.all()
            categories = BlogCategory.objects.all()
            tags = BlogTags.objects.all()
            meta_tags = BlogMetaTags.objects.all()

            for i in range(100):
                title = fake.sentence(nb_words=4, variable_nb_words=True)
                slug = slugify(title)
                content = fake.text(max_nb_chars=500)
                category = fake.random_element(categories)
                tag = fake.random_element(tags)
                meta_tag = fake.random_element(meta_tags)
                date = fake.date_between(start_date='-1y', end_date='today')
                is_hot = fake.boolean()
                likes = fake.random_int(min=0, max=1000)
                blog_image = fake.random_element(Image.objects.all())


                blog_page = BlogPage(
                    title=title,
                    slug=slug,
                    blog_content=content,
                    blog_categories=[category],
                    blog_date=date,
                    blog_is_hot=is_hot,
                    blog_likes=likes,
                    blog_image=blog_image,
                    show_in_menus=True,
                    content_type=homepage_content_type,
                )
                parent_page.add_child(instance=blog_page)
                post_page_blog_tag = PostPageBlogTags(tags=tag)
                post_page_blog_meta_tag = PostPageBlogMetaTags(
                    meta_tags=meta_tag)
                blog_author_orderable = BlogAuthorsOrderable(
                    author=blog_author,
                    page=blog_page)
                blog_page.blog_authors.add(blog_author_orderable)
                blog_page.tags.add(post_page_blog_tag)
                blog_page.meta_tags.add(post_page_blog_meta_tag)
                blog_page.save_revision().publish()


        self.stdout.write(
            self.style.SUCCESS()
