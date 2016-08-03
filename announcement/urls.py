from django.conf.urls import url
from announcement import views

urlpatterns = [
    url(r'^announcement/(?P<announcement_id>\d+)/$', views.announcement_page,
        name="announcement_page"),
]
