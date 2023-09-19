from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from indicators.models import (Indicator, IndicatorMetric,
                               Metric, Score, Reference)
from public.models import Lab, Test

User = get_user_model()

client = APIClient()


class LabObjectsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            username="exampleuser",
            password="1234abcd"
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_lab_creation(self):
        payload = {"name": "TestLab1"}
        url = reverse("api:lab-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lab.objects.count(), 1)
        self.assertEqual(Lab.objects.last().name, "TestLab1")

    def test_several_lab_creation(self):
        payload1 = {"name": "TestLab1"}
        payload2 = {"name": "TestLab2"}
        url = reverse("api:lab-list")
        response_create_1 = self.client.post(
            path=url,
            data=payload1,
            format="json"
        )
        response_create_2 = self.client.post(
            path=url,
            data=payload2,
            format="json"
        )
        response_get_1 = self.client.get(
            path=url
        )
        self.assertEqual(response_get_1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_1.data["results"]), 2)
        self.assertEqual(Lab.objects.count(), 2)

    def test_lab_get_detail(self):
        lab = Lab.objects.create(
            name="TestLab1"
        )
        url = reverse("api:lab-detail", kwargs={'pk': str(lab.id)})
        response = self.client.get(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TestLab1")

    def test_lab_soft_delete(self):
        lab = Lab.objects.create(
            name="TestLab1"
        )
        lab_count = Lab.objects.count()
        url = reverse("api:lab-detail", kwargs={'pk': str(lab.id)})
        response = self.client.delete(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lab.objects.count(), lab_count)

    def test_lab_patch(self):
        lab = Lab.objects.create(
            name="TestLab1"
        )
        url = reverse("api:lab-detail", kwargs={'pk': str(lab.id)})
        payload = {"name": "TestLab"}
        response = self.client.patch(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TestLab")


class TestObjectsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            username="exampleuser",
            password="1234abcd"
        )
        self.lab = Lab.objects.create(
            name="TestLab1"
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_test_creation(self):
        payload = {"lab_id": self.lab.id}
        url = reverse("api:test-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.count(), 1)
        self.assertEqual(response.data["lab_id"], self.lab.id)

    def test_several_test_creation(self):
        payload = {"lab_id": self.lab.id}
        url = reverse("api:test-list")
        response_create_1 = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        response_create_2 = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        response_get_1 = self.client.get(
            path=url
        )
        self.assertEqual(response_get_1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_1.data["results"]), 2)
        self.assertEqual(Test.objects.count(), 2)

    def test_lab_get_detail(self):
        test = Test.objects.create(
            lab_id=self.lab
        )
        url = reverse("api:test-detail", kwargs={'pk': str(test.id)})
        response = self.client.get(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lab_id"], self.lab.id)

    def test_test_soft_delete(self):
        test = Test.objects.create(
            lab_id=self.lab
        )
        test_count = Test.objects.count()
        url = reverse("api:test-detail", kwargs={'pk': str(test.id)})
        response = self.client.delete(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Test.objects.count(), test_count)

    def test_test_patch(self):
        test = Test.objects.create(
            lab_id=self.lab
        )
        url = reverse("api:test-detail", kwargs={'pk': str(test.id)})
        payload = {"started_at": "2023-09-17T11:22:33.654046Z"}
        response = self.client.patch(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["started_at"],
            "2023-09-17T11:22:33.654046Z"
        )
        self.assertEqual(response.data["completed_at"], None)


class IndicatorObjectsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            username="exampleuser",
            password="1234abcd"
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_indicator_creation(self):
        payload = {"name": "IndicatorName"}
        url = reverse("api:indicator-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Indicator.objects.count(), 1)
        self.assertEqual(response.data["name"], "IndicatorName")

    def test_several_indicator_creation(self):
        payload1 = {"name": "IndicatorName1"}
        payload2 = {"name": "IndicatorName2"}
        url = reverse("api:indicator-list")
        response_create_1 = self.client.post(
            path=url,
            data=payload1,
            format="json"
        )
        response_create_2 = self.client.post(
            path=url,
            data=payload2,
            format="json"
        )
        response_get_1 = self.client.get(
            path=url
        )
        self.assertEqual(response_get_1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_1.data["results"]), 2)
        self.assertEqual(Indicator.objects.count(), 2)

    def test_indicator_get_detail(self):
        indicator = Indicator.objects.create(
            name="IndicatorName"
        )
        url = reverse("api:indicator-detail", kwargs={'pk': str(indicator.id)})
        response = self.client.get(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "IndicatorName")

    def test_indicator_soft_delete(self):
        indicator = Indicator.objects.create(
            name="IndicatorName"
        )
        indicator_count = Indicator.objects.count()
        url = reverse("api:indicator-detail", kwargs={'pk': str(indicator.id)})
        response = self.client.delete(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Indicator.objects.count(), indicator_count)

    def test_indicator_patch(self):
        indicator = Indicator.objects.create(
            name="IndicatorName"
        )
        url = reverse("api:indicator-detail", kwargs={'pk': str(indicator.id)})
        payload = {"name": "IndicatorName1"}
        response = self.client.patch(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "IndicatorName1")


class MetricObjectsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            username="exampleuser",
            password="1234abcd"
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_metric_creation(self):
        payload = {
            "name": "MetricName",
            "unit": "%"
        }
        url = reverse("api:metric-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Metric.objects.count(), 1)
        self.assertEqual(response.data["name"], "MetricName")
        self.assertEqual(response.data["unit"], "%")

    def test_several_metric_creation(self):
        payload1 = {
            "name": "MetricName1",
            "unit": "%"
        }
        payload2 = {
            "name": "MetricName2",
            "unit": "km/h"
        }
        url = reverse("api:metric-list")
        response_create_1 = self.client.post(
            path=url,
            data=payload1,
            format="json"
        )
        response_create_2 = self.client.post(
            path=url,
            data=payload2,
            format="json"
        )
        response_get_1 = self.client.get(
            path=url
        )
        self.assertEqual(response_get_1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get_1.data["results"]), 2)
        self.assertEqual(Metric.objects.count(), 2)

    def test_metric_get_detail(self):
        metric = Metric.objects.create(
            name="MetricName",
            unit="%"
        )
        url = reverse("api:metric-detail", kwargs={'pk': str(metric.id)})
        response = self.client.get(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "MetricName")
        self.assertEqual(response.data["unit"], "%")

    def test_metric_soft_delete(self):
        metric = Metric.objects.create(
            name="MetricName",
            unit="%"
        )
        metric_count = Metric.objects.count()
        url = reverse("api:metric-detail", kwargs={'pk': str(metric.id)})
        response = self.client.delete(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Metric.objects.count(), metric_count)

    def test_metric_patch(self):
        metric = Metric.objects.create(
            name="MetricName",
            unit="%"
        )
        url = reverse("api:metric-detail", kwargs={'pk': str(metric.id)})
        payload = {
            "name": "MetricName1",
            "unit": "km/h"
        }
        response = self.client.patch(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "MetricName1")
        self.assertEqual(response.data["unit"], "km/h")


class IndicatorMetricObjectsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            username="exampleuser",
            password="1234abcd"
        )
        self.indicator = Indicator.objects.create(
            name="IndicatorName"
        )
        self.metric = Metric.objects.create(
            name="MetricName",
            unit="%"
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_ind_metr_creation(self):
        payload = {
            "indicator_id": self.indicator.id,
            "metric_id": self.metric.id
        }
        url = reverse("api:indicator-metric-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IndicatorMetric.objects.count(), 1)
        self.assertEqual(response.data["indicator_id"], self.indicator.id)
        self.assertEqual(response.data["metric_id"], self.metric.id)

    def test_ind_metr_get_detail(self):
        ind_metr = IndicatorMetric.objects.create(
            indicator_id=self.indicator,
            metric_id=self.metric
        )
        url = reverse(
            "api:indicator-metric-detail",
            kwargs={'pk': str(ind_metr.id)}
        )
        response = self.client.get(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["indicator_id"], self.indicator.id)
        self.assertEqual(response.data["metric_id"], self.metric.id)

    def test_ind_metr_soft_delete(self):
        ind_metr = IndicatorMetric.objects.create(
            indicator_id=self.indicator,
            metric_id=self.metric
        )
        ind_metr_count = IndicatorMetric.objects.count()
        url = reverse(
            "api:indicator-metric-detail",
            kwargs={'pk': str(ind_metr.id)}
        )
        response = self.client.delete(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IndicatorMetric.objects.count(), ind_metr_count)


class ReferenceObjectsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            username="exampleuser",
            password="1234abcd"
        )
        self.indicator = Indicator.objects.create(
            name="IndicatorName"
        )
        self.metric = Metric.objects.create(
            name="MetricName",
            unit="%"
        )
        self.ind_metr = IndicatorMetric.objects.create(
            indicator_id=self.indicator,
            metric_id=self.metric
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_reference_creation(self):
        payload = {
            "indicator_metric_id": self.ind_metr.id,
            "min_score": 10,
            "max_score": 15
        }
        url = reverse("api:reference-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reference.objects.count(), 1)
        self.assertEqual(
            response.data["indicator_metric_id"],
            self.ind_metr.id
        )

    def test_reference_min_more_than_max_creation(self):
        payload = {
            "indicator_metric_id": self.ind_metr.id,
            "min_score": 20,
            "max_score": 15
        }
        url = reverse("api:reference-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reference.objects.count(), 0)

    def test_two_references_one_ind_metr_creation(self):
        payload1 = {
            "indicator_metric_id": self.ind_metr.id,
            "min_score": 10,
            "max_score": 15
        }
        payload2 = {
            "indicator_metric_id": self.ind_metr.id,
            "min_score": 20,
            "max_score": 40
        }
        url = reverse("api:reference-list")
        response_create_1 = self.client.post(
            path=url,
            data=payload1,
            format="json"
        )
        response_create_2 = self.client.post(
            path=url,
            data=payload2,
            format="json"
        )
        self.assertEqual(
            response_create_2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Reference.objects.count(), 1)

    def test_reference_get_detail(self):
        reference = Reference.objects.create(
            indicator_metric_id=self.ind_metr,
            min_score=10,
            max_score=15
        )
        url = reverse(
            "api:reference-detail",
            kwargs={'pk': str(reference.id)}
        )
        response = self.client.get(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reference_soft_delete(self):
        reference = Reference.objects.create(
            indicator_metric_id=self.ind_metr,
            min_score=10,
            max_score=15
        )
        reference_count = Reference.objects.count()
        url = reverse(
            "api:reference-detail",
            kwargs={'pk': str(reference.id)}
        )
        response = self.client.delete(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reference.objects.count(), reference_count)


class ScoreObjectsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="user@example.com",
            username="exampleuser",
            password="1234abcd"
        )
        self.lab = Lab.objects.create(
            name="TestLab1"
        )
        self.test = Test.objects.create(
            lab_id=self.lab
        )
        self.indicator = Indicator.objects.create(
            name="IndicatorName"
        )
        self.metric = Metric.objects.create(
            name="MetricName",
            unit="%"
        )
        self.ind_metr = IndicatorMetric.objects.create(
            indicator_id=self.indicator,
            metric_id=self.metric
        )
        self.reference = Reference.objects.create(
            indicator_metric_id=self.ind_metr,
            min_score=10,
            max_score=15
        )
        self.token = Token.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_score_creation(self):
        payload = {
            "indicator_metric_id": self.ind_metr.id,
            "test_id": self.test.id,
            "score": 13
        }
        url = reverse("api:score-list")
        response = self.client.post(
            path=url,
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Score.objects.count(), 1)
        self.assertEqual(
            response.data["indicator_metric_id"],
            self.ind_metr.id
        )
        self.assertEqual(response.data["test_id"], self.test.id)

    def test_two_scores_one_test_one_ind_metr_creation(self):
        payload1 = {
            "indicator_metric_id": self.ind_metr.id,
            "test_id": self.test.id,
            "score": 13
        }
        payload2 = {
            "indicator_metric_id": self.ind_metr.id,
            "test_id": self.test.id,
            "score": 14
        }
        url = reverse("api:score-list")
        response_create_1 = self.client.post(
            path=url,
            data=payload1,
            format="json"
        )
        response_create_2 = self.client.post(
            path=url,
            data=payload2,
            format="json"
        )
        self.assertEqual(
            response_create_2.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Score.objects.count(), 1)

    def test_score_get_detail(self):
        score = Score.objects.create(
            indicator_metric_id=self.ind_metr,
            test_id=self.test,
            score=13
        )
        url = reverse(
            "api:score-detail",
            kwargs={'pk': str(score.id)}
        )
        response = self.client.get(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_score_soft_delete(self):
        score = Score.objects.create(
            indicator_metric_id=self.ind_metr,
            test_id=self.test,
            score=13
        )
        score_count = Score.objects.count()
        url = reverse(
            "api:score-detail",
            kwargs={'pk': str(score.id)}
        )
        response = self.client.delete(
            path=url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Score.objects.count(), score_count)
