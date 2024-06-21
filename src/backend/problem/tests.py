from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Problem, Tag
from question.models import Tag as QuestionTag

class ProblemViewSetTestCase(APITestCase):

    def setUp(self):
        self.tag1 = QuestionTag.objects.create(name="Tag1")
        self.tag2 = QuestionTag.objects.create(name="Tag2")
        self.problem1 = Problem.objects.create(name="Problem One", category="Algorithm")
        self.problem1.tags.add(self.tag1)
        self.problem2 = Problem.objects.create(name="Problem Two", category="System Design")
        self.problem2.tags.add(self.tag2)

    def test_filter_problems_by_name(self):
        url = reverse('practice')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
