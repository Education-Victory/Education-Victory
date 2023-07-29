from django.test import TestCase

from .models import Category, Question, Keypoint

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name='Binary Search', weight=1)

    def test_model_can_create_a_category(self):
        cate = Category.objects.get(name='Binary Search')
        self.assertEqual(cate.name, 'Binary Search')
        self.assertEqual(cate.weight, 1)
