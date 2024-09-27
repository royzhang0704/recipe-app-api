from django.test import SimpleTestCase
from . import cal

class CalSsmpletest(SimpleTestCase):
    def test_cal(self):
        res=cal.add(5,6)
        self.assertEqual(res,11)