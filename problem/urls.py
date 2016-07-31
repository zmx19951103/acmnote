from django.conf.urls import url
from problem import views

urlpatterns = [
    # fixed
    url(r'^$', views.index, name='homepage'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    # /fixed

    # fixed
    url(r'^view_note_list/$', views.view_note_list, name='view_note_list'),
    url(r'^view_problem_list/$', views.view_problem_list, name='view_problem_list'),

    url(r'view_note/(?P<pk>\d+)/$', views.view_note, name='view_note'),
    url(r'^view_problem/(?P<pk>\d+)/$', views.view_problem, name='view_problem'),

    url(r'^add_note/(\d+)/$', views.add_note, name='add_note'),


    url(r'^add_problem/$', views.add_problem, name='add_problem'),
    url(r'^add_note/$', views.add_note, name='add_note'),
    # fixed
    url(r'^add_tag/$', views.add_tag, name='add_tag'),
    # /fixed
]