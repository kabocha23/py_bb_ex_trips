from django.conf.urls import url
from . import views

urlpatterns = [
    # GET ROUTES
    url(r'^$', views.main, name='get_main'),
    url(r'^travels$', views.travels, name='get_travels'),    
    url(r'^travels/destination/(?P<id>\d+)$', views.destination, name='get_destination'),
    url(r'^travels/destination/create$', views.create, name='get_create'),
    url(r'^remove_item/(?P<id>\d+)$', views.remove_item, name='get_remove_item'),
    url(r'^delete_item/(?P<id>\d+)$', views.delete_item, name='get_delete_item'),
    url(r'^add_to_mylist/(?P<id>\d+)$', views.add_to_mylist, name='get_add_to_mylist'),   

    # POST ROUTES
    url(r'^login$', views.login, name='post_login'),
    url(r'^register$', views.register, name='post_register'),
    url(r'^travels/destination/add$', views.add_trip, name='post_add_trip'),
]