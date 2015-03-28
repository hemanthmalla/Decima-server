from django.conf.urls import url, include
from decima_server.rest_api import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^snippets/$', views.getContactsInNetwork),
    url(r'^makedecision/$', views.makeDecision),
    url(r'^createuser/$', views.createUser),
    url(r'^getquestionbyid/$', views.getQuestionById),
    url(r'^getquestionsbyuser/$', views.getQuestionsByUser),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]