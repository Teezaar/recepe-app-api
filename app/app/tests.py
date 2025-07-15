"""
Sample tests
"""
from django.test import SimpleTestCase
from rich.console import Console
console = Console()

from app import calc

class CalcTests(SimpleTestCase):
    """ Test the calc module """
    def test_add_numbers(self):
        """ Test adding numbers together """
        res = calc.add(20, 5)
        console.print(f"\nThe result from test_add_numbers: [bold green]{res}[/bold green]")

        self.assertEqual(res, 25)
