"""
Test receipe API
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    """Create and return a recipe"""

    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe
class PublicRecipeAPITests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
class PrivateRecipeAPITests(TestCase):
    """Test authenticate recipe API access"""
    def setUp(self):
        self.client = APIClient
        self.user = get_user_model().objects.create_user(
            'recipetest002@yopmail.com',
            'recipetest002'
        ) 
        self.client.force_authenticate(self.user)
    def test_retrive_recipe(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serialier = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialier.data)
    def test_recipe_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'recipetest003@yopmail.com',
            'recipetest003'
        )
        create_recipe(user=user2)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serialier = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serialier.data)
    # def test_view_recipe_detail(self):
    #     """Test viewing a recipe detail"""
    #     recipe = create_recipe(user=self.user)
    #     url = reverse('recipe:recipe-detail', args=[recipe.id])
    #     res = self.client.get(url)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)