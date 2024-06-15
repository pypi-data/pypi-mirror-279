"""Manipulate the header section."""

from lxml import etree
from typing import List
from typing import Optional

from . import config
from .base import Annotation
from .base import Extensible
from .base import Field
from .base import Form
from .base import Trait
from .base import LIFTUtilsBase
from .base import Multitext
from .datatypes import DateTime
from .datatypes import Key
from .datatypes import URL


class FieldDefn(Multitext):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``FieldDefinition``.
    """

    def __init__(
        self,
        tag: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'field'
        # attributes
        self.tag = tag

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        forms = 'forms' if len(self.form_items) > 1 else 'form'
        return f"{self.tag} ({len(self.form_items)} {forms})"

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class FieldDefinition(LIFTUtilsBase):
    """Gives information about a particular field type.
    It may be used by an application to add information not part of the LIFT
    standard.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'field'
        # attributes
        self.name: Key = None
        self.class_: Optional[str] = None
        self.type: Optional[str] = None
        self.option_range: Optional[Key] = None
        self.writing_system: Optional[str] = None
        # elements
        self.label: Optional[Multitext] = None
        self.description: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        return self.name

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class FieldDefns(LIFTUtilsBase):
    """This is a simple list of ``field-defn`` elements.

    .. note:: Used by LIFT v0.13 (FieldWorks) instead of ``Fields``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'fields'
        # elements
        self.field_items: Optional[List[FieldDefn]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class Fields(LIFTUtilsBase):
    """This is a simple list of ``field-definition`` elements.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # elements
        self.field_items: Optional[List[FieldDefinition]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class RangeElement13(LIFTUtilsBase):
    """The description of a particular range element found in a ``range``.
    """

    def __init__(
        self,
        elem_id: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'range-element'
        # attributes
        self.id = elem_id
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.description_items: Optional[List[Multitext]] = None
        self.label_items: Optional[List[Multitext]] = None
        self.abbrev_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class RangeElement(Extensible):
    """The description of a particular range element found in a ``range``.

    .. note:: Does not inherit from Extensible in LIFT v0.13 (FieldWorks).
    """

    def __init__(
        self,
        elem_id: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'range-element'
        # attributes
        self.id = elem_id
        self.parent: Key = None
        self.guid: str = None
        # elements
        self.description_items: Optional[List[Multitext]] = None
        self.label_items: Optional[List[Multitext]] = None
        self.abbrev_items: Optional[List[Multitext]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class Range13(LIFTUtilsBase):
    """A set of ``range-elements``.
    It is used to identify both the group of ``range-elements`` but also to
    some extent their type.
    """
    def __init__(
        self,
        range_id: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'range'
        # attributes
        self.id = range_id
        self.guid: Optional[str] = None
        self.href: Optional[URL] = None
        # elements
        self.description: Optional[Multitext] = None
        self.range_element_items: List[RangeElement13] = None
        self.label_items: List[Multitext] = None
        self.abbrev_items: List[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class Range(Extensible):
    """A set of ``range-elements``.
    It is used to identify both the group of ``range-elements`` but also to
    some extent their type.
    """
    def __init__(
        self,
        range_id: Key = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'range'
        # attributes
        self.id = range_id
        self.guid: Optional[str] = None
        self.href: Optional[URL] = None
        # elements
        self.description: Optional[Multitext] = None
        self.range_element_items: List[RangeElement] = None
        self.label_items: List[Multitext] = None
        self.abbrev_items: List[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class Ranges(LIFTUtilsBase):
    """The root element in a Lift Ranges file.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'ranges'
        # elements
        if config.LIFT_VERSION == '0.13':
            self.range_items: List[Range13] = None
        else:
            self.range_items: List[Range] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


class Header(LIFTUtilsBase):
    """The header information for a LIFT file.
    It includes range information and added field definitions.

    :ivar Optional[Multitext] description: Contains a multilingual description
        of the lexicon for information purposes only.
    :ivar Optional[Ranges] ranges: Contains all the ``range`` information.
    :ivar Optional[FieldDefns] field_items: `Used by LIFT v0.13 (FieldWorks).`
        Contains definitions for all the ``field`` types used in the document.
    :ivar Optional[Fields] fields: Contains definitions for all the ``field``
        types used in the document.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'header'
        # elements
        self.description: Optional[Multitext] = None
        self.ranges: Optional[Ranges] = None
        if config.LIFT_VERSION == '0.13':
            self.fields: Optional[FieldDefns] = None
        else:
            self.fields: Optional[Fields] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def __str__(self):
        s = 'Header'
        if self.description:
            s = str(self.description)
        if self.ranges and self.ranges.range_items:
            s += f": {len(self.range_items)} ranges"
        if self.fields:
            s += f", {len(self.fields)} fields"
        return s

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)


def get_properties(class_, lift_version):
    classes = (class_, *class_.__bases__)
    props = {}

    if not hasattr(class_, '__bases__'):
        print('no bases:', class_)
        return props

    props['attributes'] = {}
    props['elements'] = {}
    if Multitext in classes:
        props['elements']['form_items'] = (list, Form, False)
        props['elements']['trait_items'] = (list, Trait, False)
    if FieldDefn in classes:
        props['attributes']['tag'] = (Key, True)
    if FieldDefinition in classes:
        props['attributes']['name'] = (Key, True)
        props['attributes']['class_'] = (str, False)
        props['attributes']['type'] = (str, False)
        props['attributes']['option_range'] = (Key, False)
        props['attributes']['writing_system'] = (str, False)
        props['elements']['label'] = (Multitext, False)
        props['elements']['description'] = (Multitext, False)
    if FieldDefns in classes:
        props['elements']['field_items'] = (list, FieldDefn, False)
    if Fields in classes:
        props['elements']['field_items'] = (list, FieldDefinition, False)
    if RangeElement in classes or RangeElement13 in classes:
        props['attributes']['id'] = (Key, True)
        props['attributes']['parent'] = (Key, False)
        props['attributes']['guid'] = (str, False)
        props['elements']['description_items'] = (list, Multitext, False)
        props['elements']['label_items'] = (list, Multitext, False)
        props['elements']['abbrev_items'] = (list, Multitext, False)
    if Range in classes or Range13 in classes:
        props['attributes']['id'] = (Key, True)
        props['attributes']['guid'] = (str, False)
        props['attributes']['href'] = (URL, False)
        if lift_version == '0.13':
            props['elements']['range_element_items'] = (list, RangeElement13, True)  # noqa: E501
        else:
            props['elements']['range_element_items'] = (list, RangeElement, True)  # noqa: E501
        props['elements']['description'] = (Multitext, False)
        props['elements']['label_items'] = (list, Multitext, False)
        props['elements']['abbrev_items'] = (list, Multitext, False)
    if Ranges in classes:
        if lift_version == '0.13':
            props['elements']['range_items'] = (list, Range13, True)
        else:
            props['elements']['range_items'] = (list, Range, True)
    if Header in classes:
        props['elements']['description'] = (Multitext, False)
        props['elements']['ranges'] = (Ranges, False)
        if lift_version == '0.13':
            props['elements']['fields'] = (FieldDefns, False)
        else:
            props['elements']['fields'] = (Fields, False)
    if Extensible in classes:
        props['attributes']['date_created'] = (DateTime, False)
        props['attributes']['date_modified'] = (DateTime, False)
        props['elements']['field_items'] = (list, Field, False)
        props['elements']['trait_items'] = (list, Trait, False)
        props['elements']['annotation_items'] = (list, Annotation, False)

    return props
