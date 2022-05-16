from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rarev2api.views.auth import login_user, register_user
from rarev2api.views import PostView
from rarev2api.views.CategoryView import CategoryView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')
router.register(r'posts', PostView, 'post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login_user),
    path('register', register_user),
    path('', include(router.urls))
]
