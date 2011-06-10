from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView

import pepulator_factory.models

urlpatterns = patterns('pepulator_factory',
    url(r'^pepulators/$', ListView.as_view(
        model=pepulator_factory.models.PepulatorModel,
        template_name='pepulator_list.html',
        context_object_name='pepulators'),
        name='pepulator_list_view'),
    url(r'^pepulators/(?P<pk>\d+)/$', DetailView.as_view(
        model=pepulator_factory.models.PepulatorModel,
        template_name='pepulator_detail.html',
        context_object_name='pepulator'),
        name='pepulator_detail_view'),
    url(r'^distributors/$', ListView.as_view(
        model=pepulator_factory.models.DistributorModel,
        template_name='distributor_list.html',
        context_object_name='distributors'),
        name='distributor_list_view'),
    url(r'^distributors/(?P<pk>.+)/$', DetailView.as_view(
        model=pepulator_factory.models.DistributorModel,
        template_name='distributor_detail.html',
        context_object_name='distributor'),
        name='distributor_detail_view'),
)
