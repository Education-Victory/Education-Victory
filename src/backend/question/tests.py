# from django.test import TestCase

# from .models import Category

# class CategoryTestCase(TestCase):
#     def setUp(self):
#         Category.objects.create(name='Binary Search', weight=1)

#     def test_model_can_create_a_category(self):
#         cate = Category.objects.get(name='Binary Search')
#         self.assertEqual(cate.name, 'Binary Search')
#         self.assertEqual(cate.weight, 1)
from django.test import TestCase
from django.utils import timezone
from .models import Milestone, Question, Tag, QuestionMilestone
from problem.models import Problem 

def get_default_json():
    return {'desc': 'Default description'}

class MilestoneModelTest(TestCase):
    def setUp(self):
        self.milestone = Milestone.objects.create(name='Start')

    def test_string_representation(self):
        self.assertEqual(str(self.milestone), 'Start')

class QuestionModelTest(TestCase):
    def setUp(self):
        self.problem = Problem.objects.create(name='Sample Problem')
        self.tag = Tag.objects.create(name='Sample Tag')
        self.milestone = Milestone.objects.create(name='Start')
        self.question = Question.objects.create(problem=self.problem, desc=get_default_json())

    def test_string_representation(self):
        desc_str = self.question.desc.get('desc', '')
        expected_string = f"{self.problem.name} - {desc_str[:10]}"
        self.assertEqual(str(self.question), expected_string)

    def test_question_creation(self):
        self.assertIsInstance(self.question, Question)
        self.assertEquals(self.question.q_type, 0)  # Checking default q_type

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Greedy')

    def test_string_representation(self):
        self.assertEqual(str(self.tag), 'Greedy')
