from django.conf.urls import url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$','rest_api.views.index_controller'),
    url(r'^getContacts/$', 'rest_api.views.getContactsInNetwork'),
    url(r'^decimo/question/$', 'rest_api.views.create_question'),
    url(r'^decimo/question/(?P<key>[\d]+)/', 'rest_api.views.add_option'),
    url(r'^decimo/invite/(?P<key>[\d]+)/$', 'rest_api.views.question_invite'),
    url(r'^decima/product/post/$', 'rest_api.views.post_product'),
    url(r'^decima/product/post/(?P<key>[\d]+)/$', 'rest_api.views.post_product'),
    url(r'^decimo/(?P<key>[\d]+)/$', 'rest_api.views.decimo_question'),
    url(r'^decima/(?P<key>[\w\d\-]+)/$', 'rest_api.views.decimaMail'),
    url(r'^makedecision/$', 'rest_api.views.makeDecision'),
    url(r'^createuser/$', 'rest_api.views.createUser'),
    url(r'^submit-vote/$', 'rest_api.views.submit_vote'),
    url(r'^getquestionbyid/$', 'rest_api.views.getQuestionById'),
    url(r'^getquestionsbyuser/$', 'rest_api.views.getQuestionsByUser'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]


