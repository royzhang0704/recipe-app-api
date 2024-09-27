from django.test import SimpleTestCase
from . import cal

class  CalSimpleTest(SimpleTestCase):
    """Test the addition of two numbers."""

    def test_cal(self):
        """Test the add function."""
        res = cal.add(5, 6)
        self.assertEqual(res, 11)
