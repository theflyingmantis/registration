from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^studentp',views.studentp,name='studentp'),
    url(r'^logout_s',views.logout_s,name='logout_s'),
    url(r'^logout_f',views.logout_f,name='logout_f'),
    url(r'^studentc',views.studentc,name='studentc'),
    url(r'^facultyp/$',views.facultyp,name='facultyp'),
    url(r'^smessage/$',views.smessage,name='smessage'),
]


# How to add anything to admin. Like freeze option and also to customize the admin page.