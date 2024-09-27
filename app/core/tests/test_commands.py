"""
Test custom Django management commands.
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError

from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test custom Django management commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if the database is ready."""
        patched_check.return_value = True  # Mock check to return True, simulating the DB being ready.
        call_command('wait_for_db')  # Call the custom management command.

        # Assert that the check method was called once with the correct argument.
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep', return_value=None)  # Mock time.sleep to avoid actual delay.
    def test_wait_for_db_delay(self, patched_check, mocked_sleep):
        """Test waiting for database when getting OperationalError."""
        # Simulate Psycopg2Error twice, OperationalError three times, then success.
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # Assert that check was called 6 times (2 Psycopg2Error + 3 OperationalError + 1 success)
        self.assertEqual(patched_check.call_count, 6)

        # Assert that check was called with the correct database argument each time.
        patched_check.assert_called_with(databases=['default'])
