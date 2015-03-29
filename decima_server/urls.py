from django.conf.urls import url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = [
    url(r'^snippets/$','rest_api.views.getContactsInNetwork'),
    url(r'^decima/(?P<key>[\w\d\-]+)/', 'rest_api.views.decimaMail'),
    url(r'^makedecision/$', 'rest_api.views.makeDecision'),
    url(r'^createuser/$', 'rest_api.views.createUser'),
    url(r'^getquestionbyid/$', 'rest_api.views.getQuestionById'),
    url(r'^getquestionsbyuser/$', 'rest_api.views.getQuestionsByUser'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]