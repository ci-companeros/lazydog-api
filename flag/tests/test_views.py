"""
Unit tests for the Flag views (API endpoints).

Covers:
- List, create, retrieve, and delete flag endpoints
- Permissions for authenticated and unauthenticated users
- Proper assignment of the flagging user and admin reviewer
- Filtering, ordering, and access control
"""

from django.test import TestCase


class FlagViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up users, admin, resource, and comment for API tests.
        """
        pass

    # LIST & RETRIEVE
    def test_list_flags_authenticated(self):
        """
        Authenticated users can list their submitted flags.
        """
        pass

    def test_retrieve_flag_authenticated(self):
        """
        Authenticated users can retrieve their own flag by ID."""
        pass

    def test_retrieve_flag_unauthenticated(self):
        """Unauthenticated users cannot retrieve any flags.
        """
        pass

    def test_retrieve_flag_by_non_owner(self):
        """
        Non-owners cannot retrieve flags created by other users.
        """
        pass

    # CREATE
    def test_create_flag_on_resource(self):
        """Authenticated users can create a flag on a resource via API.
        """
        pass

    def test_create_flag_on_comment(self):
        """
        Authenticated users can create a flag on a comment via API."""
        pass

    def test_create_flag_unauthenticated(self):
        """
        Unauthenticated users cannot create flags.
        """
        pass

    def test_prevent_duplicate_flag_api(self):
        """
        API prevents users from flagging the same resource or comment twice.
        """
        pass

    # DELETE
    def test_delete_flag_by_owner(self):
        """
        Flag owner can delete their flag.
        """
        pass

    def test_delete_flag_by_non_owner(self):
        """
        Non-owners cannot delete flags they did not create.
        """
        pass

    def test_delete_flag_unauthenticated(self):
        """
        Unauthenticated users cannot delete any flags.
        """
        pass

    # ADMIN
    def test_admin_can_review_flag(self):
        """
        Admins can update the flag's status and set themselves as reviewer.
        """
        pass

