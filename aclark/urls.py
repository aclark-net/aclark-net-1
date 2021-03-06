from aclark.root import views as views_root
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import re_path
from django.contrib import admin
from rest_framework import routers
from aclark.db import urls as urls_db
from aclark.db import views as views_db

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.conf.urls.static import static

# from aclark.root.views import subscribe

router = routers.DefaultRouter()
router.register(r"clients", views_db.ClientViewSet)
router.register(r"testimonials", views_db.TestimonialViewSet)


urlpatterns = [
    url(r"^$", views_root.home, name="home"),
    url(r"^about$", views_root.about, name="about"),
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include(router.urls)),
    url(r"^db/", include(urls_db)),
    url(r"^blog$", views_root.blog, name="blog"),
    url(r"^clients$", views_root.clients, name="clients"),
    url(r"^contact$", views_root.contact, name="contact"),
    url(r"^about/team$", views_root.team, name="team"),
    url(r"^about/testimonials$", views_root.testimonials, name="testimonials"),
    url(r"^careers$", views_root.careers, name="careers"),
    url(r"^services$", views_root.services, name="services"),
    # url(r'^subscribe/', subscribe, name = "subscribe"),
    re_path(r"^cms/", include(wagtailadmin_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(r"^pages/", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = "aclark.root.views.my_custom_error_view"
