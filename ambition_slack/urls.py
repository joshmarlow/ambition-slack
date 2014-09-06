from django.conf.urls import patterns, include, url
from django.contrib import admin

from ambition_slack.github.views import GithubView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ambition_slack.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^github/', GithubView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
