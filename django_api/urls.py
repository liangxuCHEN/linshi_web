from django.conf.urls import url, include
from myApi import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^project$', views.ProjectIndexView.as_view(), name='project_index'),
    url(r'^statistics_algo$', views.statistics_algo, name='statistics_algo'),
    url(r'^single_use_rate$', views.single_use_rate, name='single_use_rate'),
    url(r'^product_use_rate$', views.product_use_rate, name='product_use_rate'),
    url(r'^single_use_rate_demo$', views.single_use_rate_demo, name='single_use_rate_demo'),
    url(r'^product_use_rate_demo$', views.product_use_rate_demo, name='product_use_rate_demo'),
    url(r'^product/(?P<p_id>\d+)/$', views.cut_detail, name='cut_detail'),
    url(r'^project_detail/(?P<p_id>\d+)/$', views.project_detail, name='project_detail'),
    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += staticfiles_urlpatterns()
