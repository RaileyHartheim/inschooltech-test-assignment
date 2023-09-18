from django.utils import timezone
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(methods=["post"], detail=True)
    def start_test(self, request):
        try:
            test = self.get_object()
            if test.completed_at:
                data = {"error": "Test was already completed"}
                return Response(
                    data=data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            test.started_at = timezone.now()
            test.save()
            return Response(
                {"message": "Test started successfully"},
                status=status.HTTP_200_OK
            )
        except Test.DoesNotExist:
            exc = exceptions.NotFound()
            data = {"error": exc.detail}
            return Response(data=data, status=exc.status_code)

    @action(methods=["post"], detail=True)
    def complete_test(self, request):
        try:
            test = self.get_object()
            if not test.started_at:
                data = {"error": "Test wasn't started"}
                return Response(
                    data=data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            test.completed_at = timezone.now()
            test.save()
            return Response(
                {"message": "Test completed successfully"},
                status=status.HTTP_200_OK
            )
        except Test.DoesNotExist:
            exc = exceptions.NotFound()
            data = {"error": exc.detail}
            return Response(data=data, status=exc.status_code)


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
