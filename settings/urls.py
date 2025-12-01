from django.apps import apps
from django.contrib import admin
from django.urls import include, path
from apps.views import welcome
from apps.views import users,city_time,counter_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name = 'welcome'),
    path('users/', users, name = 'users_list'),
    path('city_time/', city_time, name = 'city_time'),
    path('cnt/', counter_view, name='counter'),
    path('api/', include('apps.courses.urls')),
    path('api/auth/', include('rest_framework.urls',)),
]