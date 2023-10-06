"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successfull"""

        email = 'test009@yopmail.com'
        password = 'test009'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]
        for email, excepted in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, excepted)
    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test008@yopmail.com',
            'test008'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Create recipe successfully"""
        user = get_user_model().objects.create_user(
            'recipecreate001@yopmail.com',
            'receipecreate001'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample description',
        )
        self.assertEqual(str(recipe), recipe.title)
