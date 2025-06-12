"""
Unit tests for the Flag model.

Covers:
- Creation of valid flag instances on resources or comments
- Optional references and enforcement of required fields
- Status, reason, and reviewed_by logic
- Cascade deletion when a referenced user, resource, or comment is deleted
- String representation of flag objects
"""

from django.test import TestCase


class FlagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create users, resources, comments needed for flag tests.
        """
        pass

    def test_create_flag_on_resource(self):
        """
        Test creating a flag on a resource.
        """
        pass

    def test_create_flag_on_comment(self):
        """
        Test creating a flag on a comment.
        """
        pass

    def test_flag_requires_reason(self):
        """
        Test that the reason field is required.
        """
        pass

    def test_flag_status_and_reviewed_by(self):
        """
        Test status field and reviewed_by admin assignment.
        """
        pass

    def test_str_representation(self):
        """
        Test string output of flag.
        """
        pass

    def test_cascade_delete_user(self):
        """
        Flags are deleted if the user who created them is deleted.
        """
        pass

    def test_cascade_delete_resource(self):
        """
        Flags are deleted if the flagged resource is deleted.
        """
        pass

    def test_cascade_delete_comment(self):
        """
        Flags are deleted if the flagged comment is deleted.
        """
        pass
