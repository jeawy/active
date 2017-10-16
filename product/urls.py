from django.conf.urls import include, url 
from product.views import ProductView, ProductDetailView
from product import views

urlpatterns = [  
    url(r'^products/$', ProductView.as_view(), name='products'),   
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='detail'), 
    url(r'^products/(?P<pk>[0-9]+)/addatt$', views.addatt, name='addatt'),  
    url(r'^products/(?P<pk>[0-9]+)/attendcies$', views.attendcies, name='attendcies'), 
    url(r'^products/(?P<pk>[0-9]+)/setting$', views.setting, name='setting'),  
    url(r'^products/(?P<pk>[0-9]+)/change$', views.change , name='change'),   
]
