from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.begin_auth, name='login'),
    url(r'^login$', views.begin_auth, name='login'),
    url(r'^login/authenticated/$', views.twittr_authenticated, name='authenticated'),
    url(r'^accounts/(?P<username>\w+)/$', views.search_form, name='search'),
    url(r'^accounts/(?P<username>\w+)/get-tweets/$', views.search_submit, name='get-tweets'),
    url(r'^logout$', views.twittr_logout, name='logout'),

]
