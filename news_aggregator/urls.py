from django.contrib import admin
from django.urls import path
from .views import login_user, logout_user, post_story, get_stories, delete_story

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_user, name='login'),
    path('api/logout/', logout_user, name='logout'),
    path('api/stories/', post_story, name='post_story'),
    path('api/stories/get/', get_stories, name='get_stories'),
    path('api/stories/delete/<str:key>/', delete_story, name='delete_story'),
]