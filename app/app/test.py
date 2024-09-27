from django.test import SimpleTestCase
from . import cal

class  CalSsmpletest(SimpleTestCase):
    """Test add two number"""
    def test_cal(self):
        """Test funtion"""
        res = cal.add(5 , 6)
        self.assertEqual(res, 11)