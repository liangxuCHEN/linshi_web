from django.conf.urls import url, include
from myApi import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin


urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^single_use_rate$', views.single_use_rate, name='single_use_rate'),
    url(r'^single_use_rate_demo$', views.single_use_rate_demo, name='single_use_rate_demo'),
    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += staticfiles_urlpatterns()
