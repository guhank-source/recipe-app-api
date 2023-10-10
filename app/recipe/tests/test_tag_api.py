""""
Test for tag APIs
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def detail_url(tag_id):
    """return tag detail url"""
    return reverse('recipe:tag-detail', args=[tag_id])

def create_user(email='test009@yopmail.com', password='test009'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
class PrivateTagsApiTests(TestCase):
    """Test authenticate tag api"""
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    def test_retrieve_tags(self):
        """Test retrieve a list of tags"""
        Tag.objects.create(user=self.user, name='guhan')
        Tag.objects.create(user=self.user, name='guhank')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        user2 = create_user(email='recipetest003@yopmail.com',password='recipetest003')
        Tag.objects.create(user=user2, name='furity')
        tag = Tag.objects.create(user=self.user, name='Comford food')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)
    def test_update_tag(self):
        """Test updating a tag"""
        tag = Tag.objects.create(user=self.user, name='Comford food')
        payload = {'name': 'Comford food2'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])
    def test_delete_tag(self):
        """Test deleting a tag"""
        tag = Tag.objects.create(user=self.user, name='Comford food')
        url = detail_url(tag.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
    # def test_filter_tags_assigned_to_recipes(self):
    #     """Test listing tags to those assigned to recipes"""
    #     tag1 = Tag.objects.create(user=self.user, name='Breakfast')
    #     tag2 = Tag.objects.create(user=self.user, name='Lunch')
    #     recipe = create_recipe(user=self.user)
    #     recipe.tags.add(tag1)
    #     res = self.client.get(TAGS_URL, {'assigned_only': 1})
    #     serializer1 = TagSerializer(tag1)
    #     serializer2 = TagSerializer(tag2)
    #     self.assertIn(serializer1.data, res.data)
    #     self.assertNotIn(serializer2.data, res.data)