import pytest

from indicators.models import (Indicator, IndicatorMetric,
                               Metric, Score, Reference)
from public.models import Lab, Test


@pytest.mark.django_db
def test_create_lab():
    lab_count = Lab.objects.count()
    created_lab = Lab.objects.create(name="TestLab1")
    assert Lab.objects.count() == lab_count + 1
    assert created_lab.name == "TestLab1"


@pytest.mark.django_db
def test_create_test():
    test_count = Test.objects.count()
    created_lab = Lab.objects.create(name="TestLab1")
    created_test = Test.objects.create(lab_id=created_lab, comment="Test1")
    assert Test.objects.count() == test_count + 1
    assert created_test.comment == "Test1"


@pytest.mark.django_db
def test_create_indicator():
    indicator_count = Indicator.objects.count()
    created_indicator = Indicator.objects.create(
        name="TestInd1",
        description="TestInd1Desc"
    )
    assert Indicator.objects.count() == indicator_count + 1
    assert created_indicator.name == "TestInd1"
    assert created_indicator.description == "TestInd1Desc"


@pytest.mark.django_db
def test_create_metric():
    metric_count = Metric.objects.count()
    created_metric = Metric.objects.create(
        name="TestMetr1",
        unit="TestMetr1Unit"
    )
    assert Metric.objects.count() == metric_count + 1
    assert created_metric.name == "TestMetr1"
    assert created_metric.unit == "TestMetr1Unit"


@pytest.mark.django_db
def test_create_indicator_metric():
    ind_metr_count = IndicatorMetric.objects.count()
    created_indicator = Indicator.objects.create(
        name="TestInd1",
        description="TestInd1Desc"
    )
    created_metric = Metric.objects.create(
        name="TestMetr1",
        unit="TestMetr1Unit"
    )
    created_ind_metr = IndicatorMetric.objects.create(
        indicator_id=created_indicator,
        metric_id=created_metric
    )
    assert IndicatorMetric.objects.count() == ind_metr_count + 1
    assert created_ind_metr.indicator_id == created_indicator
    assert created_ind_metr.metric_id == created_metric


@pytest.mark.django_db
def test_create_score():
    score_count = Score.objects.count()
    created_lab = Lab.objects.create(name="TestLab1")
    created_test = Test.objects.create(lab_id=created_lab, comment="Test1")
    created_indicator = Indicator.objects.create(
        name="TestInd1"
    )
    created_metric = Metric.objects.create(
        name="TestMetr1",
        unit="TestMetr1Unit"
    )
    created_ind_metr = IndicatorMetric.objects.create(
        indicator_id=created_indicator,
        metric_id=created_metric
    )
    created_score = Score.objects.create(
        indicator_metric_id=created_ind_metr,
        test_id=created_test,
        score=3
    )
    assert Score.objects.count() == score_count + 1
    assert created_score.indicator_metric_id == created_ind_metr
    assert created_score.test_id == created_test
    assert created_score.score == 3


@pytest.mark.django_db
def test_create_reference():
    reference_count = Reference.objects.count()
    created_indicator = Indicator.objects.create(
        name="TestInd1"
    )
    created_metric = Metric.objects.create(
        name="TestMetr1",
        unit="TestMetr1Unit"
    )
    created_ind_metr = IndicatorMetric.objects.create(
        indicator_id=created_indicator,
        metric_id=created_metric
    )
    created_reference = Reference.objects.create(
        indicator_metric_id=created_ind_metr,
        min_score=2,
        max_score=3
    )
    assert Reference.objects.count() == reference_count + 1
    assert created_reference.indicator_metric_id == created_ind_metr
    assert created_reference.min_score == 2
    assert created_reference.max_score == 3
