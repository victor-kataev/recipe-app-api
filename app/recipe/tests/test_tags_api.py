from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag, Ingredient
from recipe.serializers import TagSerializer


TAG_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email='email@test.com', password='testing321')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        user2 = get_user_model().objects.create(email='other@user.com', password='pass321')

        Tag.objects.create(user=user2, name='Vegan')
        tag = Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        payload = {'name': 'Test name'}
        res = self.client.post(TAG_URL, payload)

        exists = Tag.objects.filter(name=payload['name'], user=self.user).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        payload = {'name': ''}
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
