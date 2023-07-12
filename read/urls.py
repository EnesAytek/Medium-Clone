from django.urls import path
from .views import all_post_view, post_detail

app_name = 'read'

urlpatterns = [
    path('<slug:user_slug>/', all_post_view, name='all_post_view' ),  
    path('<slug:user_slug>/<slug:post_slug>', post_detail, name='post_detail' ), 
]
 