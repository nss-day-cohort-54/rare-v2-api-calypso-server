from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from rarev2api.views.CategoryView import CategoryView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
