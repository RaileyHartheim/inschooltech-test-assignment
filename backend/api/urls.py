from django.urls import include, path

from .views import (IndicatorListCreateView, IndicatorMetricListCreateView,
                    IndicatorMetricObjectView, IndicatorObjectView,
                    LabListCreateView, LabObjectView,
                    MetricListCreateView, MetricObjectView,
                    ReferenceListCreateView, ReferenceObjectView,
                    ScoreListCreateView, ScoreObjectView,
                    TestListCreateView, TestObjectView)

app_name = 'api'


urlpatterns = [
    path('labs/', LabListCreateView.as_view(), name='lab-list'),
    path('labs/<uuid:id>/', LabObjectView.as_view(), name='lab-detail'),

    path('tests/', TestListCreateView.as_view(), name='test-list'),
    path('tests/<uuid:id>/', TestObjectView.as_view(), name='test-detail'),

    path(
        'indicators/',
        IndicatorListCreateView.as_view(),
        name='indicator-list'
    ),
    path(
        'indicators/<uuid:id>/',
        IndicatorObjectView.as_view(),
        name='indicator-detail'
    ),

    path('metrics/', MetricListCreateView.as_view(), name='metric-list'),
    path(
        'metrics/<uuid:id>/',
        MetricObjectView.as_view(),
        name='metric-detail'
    ),

    path(
        'indicator-metric/',
        IndicatorMetricListCreateView.as_view(),
        name='indicator-metric-list'
    ),
    path(
        'indicator-metric/<uuid:id>/',
        IndicatorMetricObjectView.as_view(),
        name='indicator-metric-detail'
    ),

    path(
        'references/',
        ReferenceListCreateView.as_view(),
        name='reference-list'
    ),
    path(
        'references/<uuid:id>/',
        ReferenceObjectView.as_view(),
        name='reference-detail'
    ),

    path('scores/', ScoreListCreateView.as_view(), name='score-list'),
    path('scores/<uuid:id>/', ScoreObjectView.as_view(), name='score-detail'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]
