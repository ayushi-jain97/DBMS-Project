from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tablename>[-\w]+)/(?P<editstring>[-\w]+)/$', views.editTable,name='editTable'),
    url(r'^(?P<tablename>[-\w]+)/', views.showTable,name='showTable'),
]


