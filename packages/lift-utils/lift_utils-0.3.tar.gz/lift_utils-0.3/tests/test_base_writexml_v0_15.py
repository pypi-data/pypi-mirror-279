# flake8: noqa: E501

import unittest
from lxml import etree

from lift_utils import base
from lift_utils import config
from lift_utils import datatypes
from lift_utils import utils
from lift_utils.lexicon import Etymology

from .utils import compare_xml_trees

LIFT_VERSION = '0.15'


class TestAnnotation(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        name = "annotation-name"
        value = "annotation-value"
        who = "Annotation Who"
        when = "0000-00-00"
        obj = base.Annotation(
            name=name,
            value=value,
            who=who,
            when=when
        )

        xml = f"""
        <annotation name="{name}" value="{value}" who="{who}" when="{when}"/>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )


class TestField(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = base.Field(name="field-type")
        obj.date_created = datatypes.DateTime("0000-00-00")
        obj.date_modified = datatypes.DateTime("0000-00-00")
        obj.annotation_items = [
            base.Annotation(
                name="",
                value="",
            ),
            base.Annotation(
                name="",
                value="",
            ),
        ]
        obj.trait_items = [
            base.Trait(name='', value=''),
            base.Trait(name='', value=''),
        ]
        obj.form_items = [
            base.Form(lang='', text=''),
            base.Form(lang='', text=''),
        ]

        xml = f"""
        <field dateCreated="{obj.date_created}" dateModified="{obj.date_modified}" name="{obj.name}">
            <form lang="">
                <text/>
            </form>
            <form lang="">
                <text/>
            </form>
            <trait name="" value=""/>
            <trait name="" value=""/>
            <annotation name="" value=""/>
            <annotation name="" value=""/>
        </field>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        # compare_xml_trees(obj._to_xml_tree(), xml_tree)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )


class TestForm(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = base.Form(lang="en", text="")
        obj.annotation_items = [
            base.Annotation(
                name="",
                value="",
            ),
            base.Annotation(
                name="",
                value="",
            ),
        ]

        xml = f"""
        <form lang="en">
            <text/>
            <annotation name="" value=""/>
            <annotation name="" value=""/>
        </form>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )


class TestGloss(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = base.Gloss(lang="", text="")
        obj.trait_items = [
            base.Trait(name="", value=""),
            base.Trait(name="", value=""),
        ]

        xml = f"""
        <gloss lang="">
            <text/>
            <trait name="" value=""/>
            <trait name="" value=""/>
        </gloss>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )


class TestSpan(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        text = "test text"
        obj = base.Span(text=text)
        obj.lang = datatypes.Lang('en')
        obj.href = datatypes.URL("https://example.com")
        obj.class_ = "TestClass"
        obj.tail = datatypes.PCData(" a tail.")

        xml = f"""
        <xml>
        <span lang="{obj.lang}" href="{obj.href}" class="{obj.class_}">{text}</span>{obj.tail}</xml>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        xml_tree = xml_tree.getchildren()[0]
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )


class TestText(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = base.Text("Test text")
        obj.span_items = [
            base.Span(text=""),
            base.Span(text=""),
        ]

        xml = f"""
        <text>Test text<span/><span/></text>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )


class TestTrait(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = base.Trait(name='TraitName', value='TraitValue')
        obj.id = datatypes.Key('TraitID')
        obj.annotation_items = [
            base.Annotation(name="", value=""),
            base.Annotation(name="", value=""),
        ]

        xml = f"""
        <trait name="TraitName" value="TraitValue" id="{obj.id}">
            <annotation name="" value=""/>
            <annotation name="" value=""/>
        </trait>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )


class TestURLRef(unittest.TestCase):
    def test_xml(self):
        config.LIFT_VERSION = LIFT_VERSION
        obj = base.URLRef(href="https://example.com")
        obj.label = base.Multitext()

        xml = f"""
        <urlref href="https://example.com">
            <label/>
        </urlref>
        """
        xml_tree = utils.xmlstring_to_etree(xml)
        self.assertEqual(
            utils.etree_to_xmlstring(obj._to_xml_tree()),
            utils.etree_to_xmlstring(xml_tree)
        )
