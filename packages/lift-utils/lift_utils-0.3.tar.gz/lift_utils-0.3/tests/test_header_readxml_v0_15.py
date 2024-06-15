import unittest
from lxml import etree

from . import DATA_PATH
from .utils import get_props
from .utils import test_attribs
from .utils import test_elems

from lift_utils import config
from lift_utils import header

HEADER_LIFT_GOOD = str(DATA_PATH / "header_good_v0.15.lift")
LIFT_VERSION = '0.15'


class TestFieldDefinition(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//field')  # noqa: E501
        self.obj = header.FieldDefinition(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.FieldDefinition, config.LIFT_VERSION)  # noqa: E501

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


class TestFields(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//fields')  # noqa: E501
        self.obj = header.Fields(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.Fields, config.LIFT_VERSION)

    def test_attribs(self):
        pass  # no attributes to test

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)

    def test_items(self):
        self.assertTrue(len(self.obj.field_items) > 1)


class TestHeader(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//header')  # noqa: E501
        self.obj = header.Header(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.Header, config.LIFT_VERSION)

    def test_attribs(self):
        pass  # no attributes to test

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)


class TestRanges(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//ranges')  # noqa: E501
        self.obj = header.Ranges(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.Ranges, config.LIFT_VERSION)

    def test_attribs(self):
        pass  # no attributes

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)

    def test_items(self):
        self.assertTrue(len(self.obj.range_items) > 1)


class TestRange(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//range')  # noqa: E501
        self.obj = header.Range(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.Range, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        optional.remove('annotation_items')
        optional.remove('field_items')
        optional.remove('trait_items')
        test_elems(self, self.obj, optional)


class TestRangeElement(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(HEADER_LIFT_GOOD).getroot().find('.//range-element')  # noqa: E501
        self.obj = header.RangeElement(xml_tree=self.xml_tree)
        self.props = header.get_properties(header.RangeElement, config.LIFT_VERSION)  # noqa: E501

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        optional.remove('annotation_items')
        optional.remove('field_items')
        optional.remove('trait_items')
        test_elems(self, self.obj, optional)
