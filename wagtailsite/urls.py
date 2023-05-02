from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls
from wagtailsite.yasg import urlpatterns as doc_patterns
from .api import api_router
from djoser import urls
from home import views as home_views
urlpatterns = [
    path('api/v2/', api_router.urls),
    path('api/v2/blog_pages/', home_views.BlogPagesApiView.as_view(),
         name='blog_pages'),
    path('api/v2/blog_pages/<slug:slug>/',
         home_views.BlogPagesApiView.as_view(), name='blog_pages_detail'),
    path('api/v2/home_page/', home_views.HomePageApiView.as_view(),
         name='home_page'),
    path('api/v2/blog_categories/', home_views.BlogCategoryListCreateView.as_view(),
         name='blog_categories'),
    path('api/v2/blog_authors/',
         home_views.BlogAuthorListCreateView.as_view(),
         name='blog_authors'),
    path('api/v2/tags/',
         home_views.BlogsTagsApiView.as_view(),
         name='blog_tags'),
    path("__reload__/", include("django_browser_reload.urls")),
    path("django-admin/", admin.site.urls),
    path(r'^admin/autocomplete/', include(autocomplete_admin_urls)),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    # path('acount/', include('allauth.urls')) # Add key in django-admin(из приложения вконтакте на лк)/


]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_patterns

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    # path("", include(wagtail_urls)),
    re_path(r'^', include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
