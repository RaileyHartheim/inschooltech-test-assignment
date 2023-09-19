from rest_framework.viewsets import generics

from indicators.models import (Indicator, IndicatorMetric,
                               Metric, Score, Reference)
from public.models import Lab, Test


from .serializers import (ChangeReferenceSerializer,
                          GetReferenceSerializer,
                          IndicatorMetricSerializer, IndicatorSerializer,
                          LabSerializer, MetricSerializer,
                          ScoreSerializer, TestSerializer,
                          TestCreateSerializer)


class LabListCreateView(generics.ListCreateAPIView):
    queryset = Lab.objects.filter(is_active=True)
    serializer_class = LabSerializer


class LabObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lab.objects.filter(is_active=True)
    serializer_class = LabSerializer


class TestListCreateView(generics.ListCreateAPIView):
    queryset = Test.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TestSerializer
        return TestCreateSerializer


class TestObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.filter(is_active=True)
    serializer_class = TestSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TestSerializer
        return TestCreateSerializer


class IndicatorListCreateView(generics.ListCreateAPIView):
    queryset = Indicator.objects.filter(is_active=True)
    serializer_class = IndicatorSerializer


class IndicatorObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Indicator.objects.filter(is_active=True)
    serializer_class = IndicatorSerializer


class MetricListCreateView(generics.ListCreateAPIView):
    queryset = Metric.objects.filter(is_active=True)
    serializer_class = MetricSerializer


class MetricObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Metric.objects.filter(is_active=True)
    serializer_class = MetricSerializer


class IndicatorMetricListCreateView(generics.ListCreateAPIView):
    queryset = IndicatorMetric.objects.filter(is_active=True)
    serializer_class = IndicatorMetricSerializer


class IndicatorMetricObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IndicatorMetric.objects.filter(is_active=True)
    serializer_class = IndicatorMetricSerializer


class ReferenceListCreateView(generics.ListCreateAPIView):
    queryset = Reference.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetReferenceSerializer
        return ChangeReferenceSerializer


class ReferenceObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reference.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetReferenceSerializer
        return ChangeReferenceSerializer


class ScoreListCreateView(generics.ListCreateAPIView):
    queryset = Score.objects.filter(is_active=True)
    serializer_class = ScoreSerializer


class ScoreObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.filter(is_active=True)
    serializer_class = ScoreSerializer
