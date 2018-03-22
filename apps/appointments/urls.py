from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^$', views.index, name="dashboard"),

	url(r'^(?P<appoint_id>[0-9]+)$', views.show, name="show"),

	url(r'^create', views.create, name="create"),

	url(r'^edit/(?P<appoint_id>[0-9]+)$', views.edit, name="edit"),

	url(r'^delete/(?P<appoint_id>[0-9]+)$', views.delete, name="delete"),
    
]
