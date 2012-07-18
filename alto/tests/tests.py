import unittest
from alto import urlviz
from alto.tests import views

class FunctionTest(unittest.TestCase):
    def test_basic_view(self):
        data = urlviz.inspect_view(views.basic_view)
        self.assertEqual(data['name'], 'basic_view')
        self.assertEqual(data['doc'], 'This is a basic test view.')
        self.assertTrue(data['file'].endswith('alto/tests/views.py'))
        self.assertTrue('line_number' in data)
        self.assertTrue('source' in data)
        self.assertTrue('sourcelines' in data)
