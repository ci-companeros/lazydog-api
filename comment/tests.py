from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from comment.models import Comment
from resource_item.models import ResourceItem


# Create your tests here.
class CommentAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Create all test data once for all tests"""
        cls.user_1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        cls.user_2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        cls.resource_item = ResourceItem.objects.create(
            title="Test Resource",
            user=cls.user_1,
        )
        cls.comment = Comment.objects.create(
            user=cls.user_1,
            resource_item=cls.resource_item,
            content="Test Comment",

@property
def id(self):
    raise NotImplementedError

@id.setter
def id(self, value):
    raise NotImplementedError


        )
        cls.url = reverse("comment-list")
        cls.url_detail = reverse("comment-detail", args=[cls.comment.id])

    def test_create_comment_success(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"content": "New Comment", "resource_item": self.resource_item.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "New Comment")
        self.assertEqual(response.data["user"], self.user_1.id)
        self.assertEqual(response.data["resource_item"], self.resource_item.id)
        self.assertEqual(Comment.objects.count(), 2)
        comment = Comment.objects.latest('id')
        self.assertEqual(comment.content, "New Comment")
        self.assertEqual(comment.user, self.user_1)
        self.assertEqual(comment.resource_item, self.resource_item)

    def test_create_comment_empty_content(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"content": "", "resource_item": self.resource_item.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_comment_missing_content(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"resource_item": self.resource_item.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)

    def test_create_comment_invalid_resource_item(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"content": "New Comment", "resource_item": 999999999999999}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_comment_missing_resource_item(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"content": "New Comment"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("resource_item", response.data)

    def test_create_comment_not_authenticated(self):
        data = {"content": "New Comment", "resource_item": self.resource_item.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)

    def test_edit_comment_by_author(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"content": "Updated Comment"}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Updated Comment")

    def test_edit_comment_by_other_user(self):
        self.client.login(username="testuser2", password="testpassword")
        data = {"content": "Updated Comment"}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Test Comment")

    def test_edit_comment_by_unauthenticated(self):
        data = {"content": "Updated Comment"}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Test Comment")

    def test_cant_edit_comment_author(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"user": self.user_2.id}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User cannot be modified.", str(response.data))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.user, self.user_1)

    def test_cant_edit_comment_resource_item(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {"resource_item": 999999999999999}
        response = self.client.patch(self.url_detail, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.resource_item, self.resource_item)

    def test_delete_comment_by_author(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_comment_by_other_user(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)

    def test_delete_comment_by_unauthenticated(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)

    def test_list_comments(self):
        Comment.objects.create(
            user=self.user_1,
            resource_item=self.resource_item,
            content="Another comment",
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_comments_by_resource_item(self):
        response = self.client.get(self.url, {"resource_item": self.resource_item.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for comment in response.data:
            self.assertEqual(comment["resource_item"], self.resource_item.id)

    def test_search_comments_by_content(self):
        response = self.client.get(self.url, {"search": "Test Comment"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_disallowed_method(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_comment_response_fields(self):
        response = self.client.get(self.url_detail)
        self.assertIn("id", response.data)
        self.assertIn("user", response.data)
        self.assertIn("resource_item", response.data)
        self.assertIn("content", response.data)
        self.assertIn("created_at", response.data)

    def test_list_comments_ordering(self):
        Comment.objects.create(
            user=self.user_1,
            resource_item=self.resource_item,
            content="Another comment",
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["content"], "Another comment")
        self.assertEqual(response.data[1]["content"], "Test Comment")
