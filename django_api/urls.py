from django.conf.urls import url
from myApi import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^single_use_rate$', views.single_use_rate, name='single_use_rate'),
]
urlpatterns += staticfiles_urlpatterns()
