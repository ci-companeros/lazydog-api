"""
Unit tests for the Tag model.

This test suite validates the data integrity and behavior of the Tag model,
including default values, uniqueness constraints, slug generation, and field
attributes.

Focus areas:
- Field definitions and defaults (e.g. description, slug)
- Auto-generated fields and timestamps
- Slug uniqueness logic
- __str__ method output
"""
from django.test import TestCase
from tag.models import Tag


class TagModelTestCase(TestCase):
    def test_str_method_returns_tag_name(self):
        """
        Test the __str__ method returns the tag's name.
        This ensures that tag instances are human-readable.
        Expected: str(tag) == tag.name
        """
        tag = Tag.objects.create(name="Test Tag")
        self.assertEqual(str(tag), "Test Tag")

    def test_slug_auto_generated_on_save(self):
        """
        Test that a slug is automatically generated when a tag is saved.
        Expected: slug field starts with a slugified version of the name.
        """
        tag = Tag.objects.create(name="Lazy Tag")
        self.assertEqual(tag.slug, "lazy-tag")

    def test_slug_uniqueness(self):
        """
        Test that slugs are unique even for tags with the same name.
        Expected: second tag with duplicate name gets a suffixed slug.

        WHY: Although 'name' must be unique, slug generation logic should
        still append a suffix for robustness in case slug clashes occur through
        manual overrides or future relaxations.
        """
        tag1 = Tag.objects.create(name="Duplicate Tag")
        tag2 = Tag.objects.create(name="Duplicate Tag")
        self.assertNotEqual(tag1.slug, tag2.slug)
        self.assertTrue(tag2.slug.startswith("duplicate-tag"))
        self.assertRegex(tag2.slug, r"^duplicate-tag-\d+$")
    def test_tag_name_must_be_unique(self):
        """
        Test that the name field enforces uniqueness.
        Expected: creating a second tag with the same name raises an error.

        WHY: Enforcing unique tag names prevents duplication and ensures
        clarity in tag-based filtering and lookup.
        """
        Tag.objects.create(name="Unique")
        with self.assertRaises(Exception):
            Tag.objects.create(name="Unique")
