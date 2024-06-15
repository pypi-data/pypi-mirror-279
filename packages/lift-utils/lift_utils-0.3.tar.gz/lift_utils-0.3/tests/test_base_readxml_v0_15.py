import unittest
from lxml import etree

from . import DATA_PATH
from .utils import get_props
from .utils import test_attribs
from .utils import test_elems

from lift_utils import base
from lift_utils import config

ENTRY_LIFT_GOOD = str(DATA_PATH / "entry_good_v0.15.lift")
LIFT_VERSION = config.LIFT_VERSION_LATEST


class TestAnnotation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = base.Annotation(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.Annotation, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        pass  # no elements


class TestExtensible(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.obj = base.Extensible(etree.parse(ENTRY_LIFT_GOOD).getroot())
        self.props = base.get_properties(base.Extensible, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)


class TestField(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//field')
        self.obj = base.Field(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.Field, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)


class TestForm(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        self.obj = base.Form(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.Form, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)


class TestGloss(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//gloss')
        self.obj = base.Gloss(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.Gloss, config.LIFT_VERSION)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)


class TestMultitext(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//annotation')  # noqa: E501
        self.obj = base.Multitext(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.Multitext, config.LIFT_VERSION)

    def test_attribs(self):
        pass  # no attribs

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        optional.remove('span_items')
        test_elems(self, self.obj, optional)


class TestSpan(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//span')
        self.obj = base.Span(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.Span, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        optional.remove('span_items')  # hard to test optional nested element
        test_elems(self, self.obj, optional)


class TestText(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//form')
        self.obj = None
        for c in self.xml_tree.getchildren():
            if c.tag == 'text':
                self.obj = base.Text(c)
                break
        if not self.obj:
            raise AssertionError
        self.props = base.get_properties(base.Text, config.LIFT_VERSION)

    def test_attribs(self):
        pass  # no attribs

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        optional.remove('span_items')  # already tested in TestSpan
        test_elems(self, self.obj, optional)


class TestTrait(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('trait')
        self.obj = base.Trait(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.Trait, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)


class TestURLRef(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(ENTRY_LIFT_GOOD).getroot().find('.//urlref')  # noqa: E501
        self.obj = base.URLRef(xml_tree=self.xml_tree)
        self.props = base.get_properties(base.URLRef, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)
