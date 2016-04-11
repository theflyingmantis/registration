from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^studentp',views.studentp,name='studentp'),
    url(r'^logout_s',views.logout_s,name='logout_s'),
    url(r'^logout_f',views.logout_f,name='logout_f'),
    url(r'^studentc/$',views.studentc,name='studentc'),
    url(r'^facultyp/$',views.facultyp,name='facultyp'),
    url(r'^smessage/$',views.smessage,name='smessage'),
    url(r'^facultyc/$',views.facultyc,name='facultyc'),
    url(r'^facultyc/(?P<id1>\d+)$',views.ffinal,name='ffinal'),
    url(r'^sfinal/$',views.sfinal,name='sfinal'),
    url(r'^confirmed/$',views.confirmed,name='confirmed'),
    url(r'^student_course/$',views.student_course,name='student_course'),
    url(r'^student_course/(?P<name>[A-Za-z1-9]+)$',views.StudentsInCourse,name='StudentsInCourse'),
    url(r'^admin_login/$',views.admin_login,name='admin_login'),
    url(r'^admin_settings/$',views.admin_settings,name='admin_settings'),
    url(r'^logout_a/$',views.logout_a,name="logout_a"),
    url(r'^course_info/$',views.course_info,name="course_info"),
    url(r'^timetable/$',views.timetable,name="timetable"),
    url(r'^accounts/$',views.accounts_login,name="accounts_login"),
    url(r'^accounts_logout/$',views.accounts_logout,name='accounts_logout'),
    url(r'^accounts_details/$',views.accounts_details,name="accounts_details"),
    url(r'^fee/$',views.fee_structure,name='fee_structure'),
]


# How to add anything to admin. Like freeze option and also to customize the admin page.