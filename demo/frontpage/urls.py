from django.conf.urls import url
from frontpage import views

urlpatterns = [
    url(r'^billboard/$',views.billboard,name ='billboard'),
    url(r'^$',views.index,name = 'index'),
]