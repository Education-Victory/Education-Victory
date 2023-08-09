from django.test import TestCase, override_settings
from django.utils import timezone
from question.models import Category, Question, Ability, Solution


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', weight=2)

    def test_category_creation(self):
        """
        Test if the Category model can be created correctly.
        """
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.weight, 2)
        self.assertLessEqual(self.category.created_at, timezone.now())
        self.assertLessEqual(self.category.updated_at, timezone.now())
        self.assertEqual(str(self.category), 'Test Category')

    def test_default_weight_value(self):
        """
        Test if the default weight value is correctly set when not provided.
        """
        default_category = Category.objects.create(name='Default Category')
        self.assertEqual(default_category.weight, 1)

    def test_category_name_max_length(self):
        """
        Test if the name field has the correct max length constraint.
        """
        max_length = Category._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)


class QuestionModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', weight=2)
        self.question = Question.objects.create(
            name='Test Question',
            description={'content': 'This is a test question.'},
            upvote=10,
            downvote=3,
            publish=True,
            URL='http://example.com/test',
        )
        self.question.category_id_list.add(self.category)

    def test_question_creation(self):
        """
        Test if the Question model can be created correctly.
        """
        self.assertEqual(self.question.name, 'Test Question')
        self.assertEqual(self.question.description, {'content': 'This is a test question.'})
        self.assertEqual(self.question.upvote, 10)
        self.assertEqual(self.question.downvote, 3)
        self.assertTrue(self.question.publish)
        self.assertEqual(self.question.URL, 'http://example.com/test')
        self.assertLessEqual(self.question.created_at, timezone.now())
        self.assertLessEqual(self.question.updated_at, timezone.now())
        self.assertEqual(str(self.question), 'Test Question')

    def test_question_category_relationship(self):
        """
        Test if the question is associated with the correct category.
        """
        self.assertEqual(self.question.category_id_list.count(), 1)
        self.assertEqual(self.question.category_id_list.first(), self.category)

    def test_default_upvote_and_downvote_value(self):
        """
        Test if the default upvote and downvote values are correctly set when not provided.
        """
        default_question = Question.objects.create(name='Default Question',
                                                   description={'content': 'This is a test question.'})
        self.assertEqual(default_question.upvote, 1)
        self.assertEqual(default_question.downvote, 1)

    def test_question_name_max_length(self):
        """
        Test if the name field has the correct max length constraint.
        """
        max_length = Question._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_question_url_max_length(self):
        """
        Test if the URL field has the correct max length constraint.
        """
        max_length = Question._meta.get_field('URL').max_length
        self.assertEqual(max_length, 20)

@override_settings(VALID_ABILITY_KEYS=['binary tree', 'heap', 'linked list'])
class AbilityModelTest(TestCase):

    def test_ability_creation(self):
        """
        Test if the Ability model can be created correctly.
        """
        ability_data = {
            'binary tree': 10,
            'linked list': 5,
            'heap': 8,
        }
        ability = Ability.objects.create(ability=ability_data)

        # Check if the Ability object is created with the correct data
        self.assertEqual(ability.ability, ability_data)


    def test_default_ability_creation(self):
        """
        Test if the Ability model is created with default values when no data is provided.
        """
        default_ability = Ability.objects.create()

        # Check if the default Ability object is created with the default values
        self.assertEqual(default_ability.ability, {
            'binary tree': 0,
            'linked list': 0,
            'heap': 0,
        })

    def test_invalid_ability_keys(self):
        """
        Test if the Ability model raises an error when invalid keys are provided.
        """
        invalid_ability_data = {
            'binary tree': 0,
            'linked list': 0,
            'invalid_key': 8,
        }

        with self.assertRaises(Exception) as context:
            Ability.objects.create(ability=invalid_ability_data)

        self.assertIn("Invalid key: invalid_key", str(context.exception))

    def test_add_missing_keys_with_default_value(self):
        """
        Test if the Ability model adds missing keys with default values when not provided.
        """
        ability_data_missing_keys = {
            'binary tree': 10,
            'linked list': 5,
        }

        ability = Ability.objects.create(ability=ability_data_missing_keys)

        # Check if the missing keys are added with default values (0)
        self.assertEqual(ability.ability, {
            'binary tree': 10,
            'linked list': 5,
            'heap': 0,
        })


    def test_save_method_with_existing_ability(self):
        """
        Test the save method when ability is already defined.
        """
        ability_data = {
            'binary tree': 10,
            'linked list': 5,
            'heap': 8,
        }

        ability = Ability.objects.create(ability=ability_data)

        # Update ability with new data
        updated_ability_data = {
            'binary tree': 12,
            'linked list': 6,
            'heap': 9,
        }
        ability.ability = updated_ability_data
        ability.save()

        # Check if the ability is updated correctly
        updated_ability = Ability.objects.get(pk=ability.pk)
        self.assertEqual(updated_ability.ability, updated_ability_data)

    def test_save_method_with_empty_ability(self):
        """
        Test the save method when ability is empty.
        """
        empty_ability = Ability()
        empty_ability.save()

        # Check if the ability is initialized with default values
        self.assertEqual(empty_ability.ability, {
            'binary tree': 0,
            'linked list': 0,
            'heap': 0,
        })


@override_settings(VALID_ABILITY_KEYS=['binary tree', 'heap', 'linked list'])
class SolutionModelTest(TestCase):

    def setUp(self):
        # Create a test Category
        self.category = Category.objects.create(name='Test Category', weight=2)

        # Create a test Question
        self.question = Question.objects.create(
            name='Test Question', description={'text': 'This is a test question'}, publish=True)

        # Create a test Ability
        self.ability = Ability.objects.create(ability={'binary tree': 10, 'heap': 8, 'linked list': 5})

    def test_solution_creation(self):
        """
        Test if the Solution model can be created correctly.
        """
        solution_data = {
            'name': 'Test Solution',
            'question_id': self.question,
            'ability_id': self.ability,
            'type': Solution.SolutionType.CODING,
            'answer': {'text': 'This is a test solution'},
            'resources': {'link': 'http://test-resource.com'},
        }

        solution = Solution.objects.create(**solution_data)
        # Add related categories using set() method
        solution.category_id_list.set([self.category])
        self.assertEqual(solution.name, 'Test Solution')
        self.assertEqual(solution.question_id, self.question)
        self.assertEqual(list(solution.category_id_list.all()), [self.category])
        self.assertEqual(solution.ability_id, self.ability)
        self.assertEqual(solution.type, Solution.SolutionType.CODING)
        self.assertEqual(solution.answer, {'text': 'This is a test solution'})
        self.assertEqual(solution.resources, {'link': 'http://test-resource.com'})
        self.assertIsNotNone(solution.created_at)
        self.assertIsNotNone(solution.updated_at)
        self.assertLessEqual(solution.created_at, timezone.now())
        self.assertLessEqual(solution.updated_at, timezone.now())

    def test_solution_str_method(self):
        """
        Test the __str__ method of the Solution model.
        """
        solution_data = {
            'name': 'Test Solution',
            'question_id': self.question,
            'type': Solution.SolutionType.CODING,
            'answer': {'text': 'This is a test solution'},
            'resources': {'link': 'http://test-resource.com'},
        }

        solution = Solution.objects.create(**solution_data)

        # Add related categories using set() method
        solution.category_id_list.set([self.category])
        expected_str = 'Test Solution - Test Question'
        self.assertEqual(str(solution), expected_str)