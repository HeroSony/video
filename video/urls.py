from django.urls import path
from .views import (
    IndexView,
    PostDetailView,
    dmca,
    statement,
    contact,
    flash,
    search,
    # tags,
)
from django.conf.urls import include, url

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    url(r'^item/(?P<pk>\d+)/$',
        PostDetailView.as_view(),
        name="video"),

    # path('', index, name='index'),
    # path('item/<int:video_id>', video, name='video'),
    path('dmca', dmca, name='dmca'),
    path('statement', statement, name='statement'),
    path('contact', contact, name='contact'),

    path('flash', flash, name='flash'),
    path('search', search, name='search'),
    # path('tags', tags, name='tags'),
]
