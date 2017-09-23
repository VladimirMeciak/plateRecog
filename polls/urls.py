from django.conf.urls import url


from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^loaddb/$', views.loaddb, name='loaddb'),
    url(r'^plates/$', views.showPlates, name='plates'),
    url(r'^visitors/$', views.showVisitors, name='visitors'),
    url(r'^corrected/(?P<pk>[0-9]+)/$', views.showCorrected, name='corrected'),
    url(r'^show/$', views.show, name='show'),
    url(r'^detail_visitor/(?P<spz>[a-zA-Z0-9_]+)/$', views.detail_visitor, name='detail_visitor'),
    url(r'^visitor_edit/$', views.visitor_new, name='visitor_new'),
    url(r'^visitor_edit/(?P<spz>[a-zA-Z0-9_]+)/$', views.visitor_edit, name='visitor_edit'),
    url(r'^detail_plate/(?P<pk>[0-9]+)/$', views.detail_plate, name='detail_plate'),

]
