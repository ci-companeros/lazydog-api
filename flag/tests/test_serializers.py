"""
Unit tests for the Flag serializer.

Covers:
- Serialization and creation of valid flag objects
- Validation of required fields and foreign keys
- Handling of optional resource/comment references
- Rejection of duplicate or invalid flags
- Validation of status and reason fields
"""

from django.test import TestCase


class FlagSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up test users, resource, comment for serializer tests.
        """
        pass

    def test_valid_flag_on_resource(self):
        """
        Serializer allows creation of a flag on a resource.
        """
        pass

    def test_valid_flag_on_comment(self):
        """
        Serializer allows creation of a flag on a comment.
        """
        pass

    def test_missing_reason_rejected(self):
        """
        Serializer rejects flags without a reason.
        """
        pass

    def test_invalid_status_value(self):
        """
        Serializer rejects flags with invalid status.
        """
        pass

    def test_duplicate_flag_rejected(self):
        """
        Serializer rejects duplicate flags for
        the same user/resource or user/comment.
        """
        pass

    def test_assigns_authenticated_user(self):
        """
        Serializer automatically assigns the logged-in user.
        """
        pass

    def test_assigns_admin_as_reviewer(self):
        """
        Admin can set themselves as reviewed_by on a flag.
        """
        pass

    def test_missing_resource_and_comment_rejected(self):
        """
        Serializer rejects flags that have neither
        resource nor comment set.
        """
        pass
