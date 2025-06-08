"""
Unit tests for the ResourceItem model.

This test suite ensures correct creation, constraint handling, relationships,
and business logic for the ResourceItem model.

Covered cases:
- Creation with all and minimal fields
- Unique constraint for url
- Many-to-many tags
- Optional category
- Field length constraint for description
- String representation
- Default ordering (by created_at desc)
"""

from django.test import TestCase
from django.contrib.auth.models import User
from category.models import Category
from tag.models import Tag
from resource_item.models import ResourceItem
from django.db import IntegrityError, transaction


class ResourceItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up common objects: user, category (HTML), and tag (python)."""
        cls.user = User.objects.create_user(
            username="testuser", password="testpw"
        )
        cls.category_html = Category.objects.create(name="HTML")
        cls.tag_python = Tag.objects.create(name="python")

    def test_create_resourceitem_with_all_fields(self):
        """Should create a ResourceItem with all fields and assign a tag."""
        item = ResourceItem.objects.create(
            title="HTML Crash Course",
            description="A guide to HTML basics.",
            category=self.category_html,
            user=self.user,
            url="https://html.com"
        )
        item.tags.add(self.tag_python)
        self.assertEqual(item.title, "HTML Crash Course")
        self.assertEqual(item.category, self.category_html)
        self.assertEqual(item.user, self.user)
        self.assertIn(self.tag_python, item.tags.all())
        self.assertIsNotNone(item.created_at)
        self.assertIsNotNone(item.updated_at)
        self.assertEqual(str(item), "HTML Crash Course")

    def test_create_resourceitem_minimal_fields(self):
        """
        Should create a ResourceItem with minimal fields
        (category and tags optional).
        """
        item = ResourceItem.objects.create(
            title="No Category",
            description="No category for this resource.",
            category=None,
            user=self.user,
            url="https://nocat.com"
        )
        self.assertIsNone(item.category)
        self.assertEqual(item.title, "No Category")

    def test_unique_url_constraint(self):
        """Should not allow two ResourceItems with the same url
        (unique constraint)."""
        ResourceItem.objects.create(
            title="HTML1",
            description="desc1",
            category=self.category_html,
            user=self.user,
            url="https://unique.com"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():  
                ResourceItem.objects.create(
                    title="HTML2",
                    description="desc2",
                    category=self.category_html,
                    user=self.user,
                    url="https://unique.com"  # Duplicate url
                )

    def test_description_max_length_constraint(self):
        """Should raise error if description is longer than 500 chars."""
        too_long = "a" * 501
        item = ResourceItem(
            title="Too Long",
            description=too_long,
            category=self.category_html,
            user=self.user,
            url="https://longdesc.com"
        )
        with self.assertRaises(Exception):
            item.full_clean()

    def test_many_to_many_tags(self):
        """Should be able to assign multiple tags to a ResourceItem."""
        tag_django = Tag.objects.create(name="django")
        item = ResourceItem.objects.create(
            title="Tagged Resource",
            description="Resource with multiple tags.",
            category=self.category_html,
            user=self.user,
            url="https://tags.com"
        )
        item.tags.add(self.tag_python, tag_django)
        self.assertEqual(item.tags.count(), 2)
        self.assertIn(tag_django, item.tags.all())
        self.assertIn(self.tag_python, item.tags.all())

    def test_str_method(self):
        """__str__ should return the resource title."""
        item = ResourceItem.objects.create(
            title="Check String",
            description="Check string output.",
            category=self.category_html,
            user=self.user,
            url="https://str.com"
        )
        self.assertEqual(str(item), "Check String")

    def test_default_ordering_by_created_at_desc(self):
        """Should order ResourceItems by -created_at by default
        (newest first)."""
        item1 = ResourceItem.objects.create(
            title="First",
            description="First item",
            category=self.category_html,
            user=self.user,
            url="https://first.com"
        )
        item2 = ResourceItem.objects.create(
            title="Second",
            description="Second item",
            category=self.category_html,
            user=self.user,
            url="https://second.com"
        )
        qs = ResourceItem.objects.all()
        self.assertEqual(qs.first(), item2)
        self.assertEqual(qs.last(), item1)
