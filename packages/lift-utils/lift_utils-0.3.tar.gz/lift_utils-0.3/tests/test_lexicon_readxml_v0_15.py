import unittest
from lxml import etree

from . import DATA_PATH
from .utils import get_props
from .utils import test_attribs
from .utils import test_elems

from lift_utils import config
from lift_utils import lexicon

LIFT_GOOD = str(DATA_PATH / "lexicon_good_v0.15.lift")
LIFT_VERSION = '0.15'


class TestEntry(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//entry')
        self.obj = lexicon.Entry(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Entry, config.LIFT_VERSION)

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


class TestEtymology(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//etymology')
        self.obj = lexicon.Etymology(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Etymology, config.LIFT_VERSION)  # noqa: E501

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


class TestExample(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//example')
        self.obj = lexicon.Example(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Example, config.LIFT_VERSION)  # noqa: E501

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


class TestGrammaticalInfo(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//grammatical-info')  # noqa: E501
        self.obj = lexicon.GrammaticalInfo(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.GrammaticalInfo, config.LIFT_VERSION)  # noqa: E501

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


class TestLexicon(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot()
        self.obj = lexicon.Lexicon(path=LIFT_GOOD, xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Lexicon, config.LIFT_VERSION)  # noqa: E501

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


class TestNote(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//note')
        self.obj = lexicon.Note(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Note, config.LIFT_VERSION)

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        pass  # no elements


class TestPhonetic(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//pronunciation')  # noqa: E501
        self.obj = lexicon.Phonetic(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Phonetic, config.LIFT_VERSION)  # noqa: E501

    def test_attribs(self):
        pass  # no attributes

    def test_elems(self):
        required = get_props(self.props, prop_type='elements')
        test_elems(self, self.obj, required)
        optional = get_props(self.props, prop_type='elements', optional=True)
        test_elems(self, self.obj, optional)


class TestRelation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//relation')
        self.obj = lexicon.Relation(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Relation, config.LIFT_VERSION)  # noqa: E501

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


class TestReversal(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//reversal')
        self.obj = lexicon.Reversal(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Reversal, config.LIFT_VERSION)  # noqa: E501

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


class TestSense(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//sense')
        self.obj = lexicon.Sense(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Sense, config.LIFT_VERSION)

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


class TestTranslation(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//translation')
        self.obj = lexicon.Translation(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Translation, config.LIFT_VERSION)  # noqa: E501

    def test_attribs(self):
        required = get_props(self.props, prop_type='attributes')
        test_attribs(self, self.obj, required)
        optional = get_props(self.props, prop_type='attributes', optional=True)
        test_attribs(self, self.obj, optional)

    def test_elems(self):
        pass  # no elements


class TestVariant(unittest.TestCase):
    def setUp(self):
        config.LIFT_VERSION = LIFT_VERSION
        self.xml_tree = etree.parse(LIFT_GOOD).getroot().find('.//variant')
        self.obj = lexicon.Variant(xml_tree=self.xml_tree)
        self.props = lexicon.get_properties(lexicon.Variant, config.LIFT_VERSION)  # noqa: E501

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
