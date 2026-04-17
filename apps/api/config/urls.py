from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include("wagtail.admin.urls")),
    path("documents/", include("wagtail.documents.urls")),
]
