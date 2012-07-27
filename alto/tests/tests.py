import unittest
from django.core.urlresolvers import RegexURLPattern
from alto import urlviz
from alto.tests import views


# urlpatterns #################################################################

class BasicPatternTest(unittest.TestCase):
    def setUp(self):
        self.pattern = RegexURLPattern(r'^test/$', views.basic_view)

    def test_pattern(self):
        self.assertEqual(self.pattern.regex.pattern, r'^test/$')
        self.assertEqual(self.pattern.callback, views.basic_view)
        self.assertEqual(self.pattern.name, None)
        self.assertEqual(self.pattern.default_args, {})

    def test_inspect_pattern(self):
        data = urlviz.inspect_pattern(self.pattern)
        self.assertEqual(data['regex'], r'^test/$')
        self.assertEqual(data['name'], None)
        self.assertEqual(data['view_module'], 'alto.tests.views')
        self.assertEqual(data['view_name'], 'basic_view')
        self.assertEqual(data['prefix'], '')
        self.assertEqual(data['default_args'], {})

class BasicStringPatternTest(unittest.TestCase):
    def setUp(self):
        self.pattern = RegexURLPattern(r'^test/$', 'alto.tests.views.basic_view')

    def test_pattern(self):
        self.assertEqual(self.pattern.callback, views.basic_view)

    def test_inspect_pattern(self):
        data = urlviz.inspect_pattern(self.pattern)
        self.assertEqual(data['view_module'], 'alto.tests.views')
        self.assertEqual(data['view_name'], 'basic_view')

class BasicNamedPatternTest(unittest.TestCase):
    def setUp(self):
        self.pattern = RegexURLPattern(r'^test/$', views.basic_view, name='test')

    def test_pattern(self):
        self.assertEqual(self.pattern.name, 'test')

    def test_inspect_pattern(self):
        data = urlviz.inspect_pattern(self.pattern)
        self.assertEqual(data['name'], 'test')

class BasicDefaultArgsPatternTest(unittest.TestCase):
    def setUp(self):
        self.args = {'template': 'test.html'}
        self.pattern = RegexURLPattern(r'^test/$', views.basic_view, default_args=self.args)

    def test_pattern(self):
        self.assertEqual(self.pattern.default_args, self.args)

    def test_inspect_pattern(self):
        data = urlviz.inspect_pattern(self.pattern)
        self.assertEqual(data['default_args'], self.args)

class BasicCaptureGroupTest(unittest.TestCase):
    def test_positional_arg(self):
        pattern = RegexURLPattern(r'^positional/(\d+)/$', views.single_positional_arg)
        data = urlviz.inspect_pattern(pattern)
        self.assertEqual(data['annotated_pattern'],
            'positional/<span class="capturegroup">&lt;id&gt;</span>/')
        self.assertEqual(data['normalized_pattern'], 'positional/id/')
        self.assertEqual(data['raw_pattern'], r'^positional/(\d+)/$')

    def test_keyword_arg(self):
        pattern = RegexURLPattern(r'^keyword/(?P<slug>\w+)/$', views.single_keyword_arg)
        data = urlviz.inspect_pattern(pattern)
        self.assertEqual(data['annotated_pattern'],
            'keyword/<span class="capturegroup">&lt;slug&gt;</span>/')
        self.assertEqual(data['normalized_pattern'], 'keyword/slug/')
        self.assertEqual(data['raw_pattern'], r'^keyword/(?P<slug>\w+)/$')

class IncludedPatternTest(unittest.TestCase):
    def test_included_pattern(self):
        p = urlviz.inspect_urlpatterns()[2]
        self.assertEqual(p['raw_pattern'], '^testapp/basic_view/$')
        self.assertEqual(p['normalized_pattern'], 'testapp/basic_view/')
        self.assertEqual(p['annotated_pattern'], 'testapp/basic_view/')

class ResolverTest(unittest.TestCase):
    def test_settings_resolver(self):
        data = urlviz.inspect_urlpatterns()
        self.assertEqual(len(data), 4)

# Views #######################################################################

class FunctionTest(unittest.TestCase):
    def test_basic_view(self):
        view, decorators = urlviz.extract_view(views.basic_view)
        data = urlviz.inspect_view(view)
        self.assertEqual(data['name'], 'basic_view')
        self.assertEqual(data['doc'], 'This is a basic test view.')
        self.assertTrue(data['file'].endswith('alto/tests/views.py'))
        self.assertTrue('line_number' in data)
        self.assertTrue('source' in data)
        self.assertTrue('sourcelines' in data)

class DecoratedFunctionTest(unittest.TestCase):
    def test_extract_view(self):
        view, decorators = urlviz.extract_view(views.decorated_view)
        data = urlviz.inspect_view(view)
        self.assertEqual(data['name'], 'decorated_view')
        self.assertEqual(data['doc'], 'This is a decorated function view.')
        self.assertTrue(data['file'].endswith('alto/tests/views.py'))

class ClassTest(unittest.TestCase):
    def test_class_view(self):
        view, decorators = urlviz.extract_view(views.ClassView())
        data = urlviz.inspect_view(view)
        self.assertEqual(data['name'], 'ClassView')
        self.assertEqual(data['doc'], 'This is a basic class view.')
        self.assertTrue(data['file'].endswith('alto/tests/views.py'))
