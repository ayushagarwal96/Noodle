from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update_user/$', views.update_user, name='update_user'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = 'detail'),
    url(r'^create_book/$', views.create_book, name='create_book'),
    url(r'(?P<pk>[0-9]+)/update_book/$', views.BookUpdate.as_view(), name='update_book'),
    url(r'^(?P<book_id>[0-9]+)/delete_book/$', views.delete_book, name='delete_book'),
    url(r'^charts/$', views.charts, name='charts'),


]