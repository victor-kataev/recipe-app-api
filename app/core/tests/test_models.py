from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag, Ingredient


def sample_user(email='email@test.com', password='testing321'):
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'random@email.com'
        password = 'Testing321'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        email = 'random@eMaIL.COM'
        user = get_user_model().objects.create_user(email, 'testing321')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testing321')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'testing321'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_tag_str(self):
        tag = Tag.objects.create(user=sample_user(), name='Vegan')
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEquals(str(ingredient), ingredient.name)
