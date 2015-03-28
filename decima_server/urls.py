from django.conf.urls import url, include
from django.contrib import admin

from rest_api import views

admin.autodiscover()

urlpatterns = [
    url(r'^snippets/$', views.getContactsInNetwork),
    url(r'^decima/(?P<key>[\w\d\-]+)/', views.decimaMail),
    url(r'^makedecision/$', views.makeDecision),
    url(r'^createuser/$', views.createUser),
    url(r'^getquestionbyid/$', views.getQuestionById),
    url(r'^getquestionsbyuser/$', views.getQuestionsByUser),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]