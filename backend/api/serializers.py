from django.utils import timezone
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from indicators.models import (Indicator, IndicatorMetric,
                               Metric, Score, Reference)
from public.models import Lab, Test
from users.models import User


class LabSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lab
        fields = "__all__"


class IndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        fields = "__all__"


class MetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metric
        fields = "__all__"


class IndicatorMetricSerializer(serializers.ModelSerializer):
    indicator_name = serializers.SerializerMethodField()
    metric_name = serializers.SerializerMethodField()
    metric_unit = serializers.SerializerMethodField()

    class Meta:
        model = IndicatorMetric
        fields = (
            "id",
            "indicator_id",
            "indicator_name",
            "metric_id",
            "metric_name",
            "metric_unit",
            "is_active"
        )

    def get_indicator_name(self, obj):
        return obj.indicator_id.name

    def get_metric_name(self, obj):
        return obj.metric_id.name

    def get_metric_unit(self, obj):
        return obj.metric_id.unit


class BaseScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = (
            "id",
            "score"
        )


class ScoreSerializer(BaseScoreSerializer):

    class Meta:
        model = Score
        fields = (
            "test_id",
            "indicator_metric_id",
            "is_active"
        ) + BaseScoreSerializer.Meta.fields


class ScoreInTestSerializer(BaseScoreSerializer):
    indicator_name = serializers.SerializerMethodField()
    metric_name = serializers.SerializerMethodField()
    metric_unit = serializers.SerializerMethodField()
    is_within_normal_range = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = (
            "indicator_name",
            "metric_name",
            "metric_unit",
            "is_within_normal_range"
        ) + BaseScoreSerializer.Meta.fields

    def get_indicator_name(self, obj):
        return obj.indicator_metric_id.indicator_id.name

    def get_metric_name(self, obj):
        return obj.indicator_metric_id.metric_id.name

    def get_metric_unit(self, obj):
        return obj.indicator_metric_id.metric_id.unit

    def get_is_within_normal_range(self, obj):
        # TODO: what about edge case when reference doesn't exist?
        normal_range = Reference.objects.get(
            indicator_metric_id=obj.indicator_metric_id
        )
        range_min = normal_range.min_score
        range_max = normal_range.max_score
        return range_max >= obj.score >= range_min


class BaseReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reference
        fields = (
            "id",
            "min_score",
            "max_score",
            "is_active"
        )


class GetReferenceSerializer(BaseReferenceSerializer):
    indicator_metric_pair = IndicatorMetricSerializer(
        source="indicator_metric_id"
    )

    class Meta:
        model = Reference
        fields = BaseReferenceSerializer.Meta.fields + ("indicator_metric_pair",)

    def get_indicator_metric_pair(self, obj):
        return IndicatorMetricSerializer(
            IndicatorMetric.objects.get(id=obj.indicator_metric_id)
        ).data


class ChangeReferenceSerializer(BaseReferenceSerializer):

    class Meta:
        model = Reference
        fields = BaseReferenceSerializer.Meta.fields + ("indicator_metric_id",)

    def validate(self, data):

        if (
            data["min_score"] is not None and data["max_score"] is not None
            and data["min_score"] > data["max_score"]
        ):
            raise serializers.ValidationError(
                "Min score can't be more than max score!"
            )

        return data


class TestSerializer(serializers.ModelSerializer):
    duration_seconds = serializers.SerializerMethodField()
    results = ScoreInTestSerializer(source="scores", read_only=True, many=True)

    class Meta:
        model = Test
        fields = (
            "id",
            "lab_id",
            "duration_seconds",
            "results"
        )

    def get_duration_seconds(self, obj):
        if not obj.started_at and not obj.completed_at:
            return 0

        start_time = obj.started_at if obj.started_at else timezone.now()
        completion_time = obj.completed_at if obj.completed_at else timezone.now()

        duration_seconds = completion_time - start_time

        return duration_seconds


class TestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = (
            "id",
            "lab_id",
            "started_at",
            "completed_at"
        )


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True},
                        "first_name": {"required": False},
                        "last_name": {"required": False},
                        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )
