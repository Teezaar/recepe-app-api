"""
Test cusom Django management commands
"""

from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error


# Mock the database behavior
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    #
    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for db when db is available. This test basically checks
        we call the right thing from test_wait_for_db_ready
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        # make sure the mock object called with these parameters
        patched_check.assert_called_once_with(databases=['default'])

    # check db wait check again after a delay but in test we mock the sleep
    # we don't want to wait for real time
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""

        # we want to simulate the database not being ready we use side effect
        # we raise Psycopg2Error twice and OperationalError 3 and True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # 2 + 3 + 1 = 6 calls to check
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
