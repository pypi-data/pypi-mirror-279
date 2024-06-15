"""Manipulate base linguistic elements."""

import sys
from lxml import etree
from typing import List
from typing import Optional

from . import config
from .datatypes import PCData
from .datatypes import DateTime
from .datatypes import Key
from .datatypes import Lang
from .datatypes import URL
from .errors import RequiredValueError
from .utils import etree_to_obj_attributes
from .utils import etree_to_xmlstring
from .utils import obj_attributes_to_etree


class LIFTUtilsBase:
    """This is a base class for all LIFT-related objects in this package.

    :ivar etree._Element xml_tree: The object's current data.
    """

    def __init__(self, xml_tree: etree._Element = None):
        self._xml_tag = None
        # self.props = Props(attributes=list(), elements=list())

    def print(self, _format='xml'):
        """Print the object's data to stdout; as XML by default."""
        try:
            if _format == 'xml':
                print(self._to_xml(), flush=True)
            else:
                return
        except BrokenPipeError:
            sys.stdout = None

    def _add_list_item(self, _name, _class, **kwargs):
        new_obj = _class(**kwargs)
        if self.__dict__.get(_name) is None:
            self.__dict__[_name] = [new_obj]
        else:
            self.__dict__[_name].append(new_obj)
        return new_obj

    def _get_properties(self):
        return get_properties(self.__class__, config.LIFT_VERSION)

    def _update_from_xml(self, xml_tree):
        # Update object attributes.
        etree_to_obj_attributes(
            xml_tree,
            self,
            self._get_properties()
        )

    def _to_xml_tree(self):
        xml_tree = obj_attributes_to_etree(
            self,
            self._xml_tag,
            self._get_properties()
        )
        return xml_tree

    def _to_xml(self, xml_tree=None):
        if xml_tree is None:
            xml_tree = self._to_xml_tree()
        return etree_to_xmlstring(xml_tree)

    def show(self):
        """Print an overview of the object in the terminal window."""
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                print(f"{k}: {v}")


class Span(LIFTUtilsBase):
    """A Unicode string marked with language and formatting information.
    """

    def __init__(
        self,
        text: str = None,
        tail: str = None,
        lang: str = None,
        href: str = None,
        span_class: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'span'
        # attributes
        self.lang: Optional[Lang] = None
        self.href: Optional[URL] = None
        self.class_: Optional[str] = None
        # elements
        self.pcdata: PCData = None
        self.tail: Optional[PCData] = None
        self.span_items: Optional[List[Span]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif text is not None:
            self.pcdata = PCData(text)
            if tail is not None:
                self.tail = PCData(tail)
            if lang is not None:
                self.lang = Lang(lang)
            if href is not None:
                self.href = URL(href)
            if span_class is not None:
                self.class_ = span_class
        else:
            raise RequiredValueError(('text',))

    def __str__(self):
        s = self.pcdata
        if self.span_items:
            for item in self.span_items:
                s += item.pcdata
                if item.tail:
                    s += item.tail
        if self.tail:
            s += self.tail


class Trait(LIFTUtilsBase):
    """An important mechanism for giving type information to an object.
    It can also be used for adding binary constraints.
    """

    def __init__(
        self,
        name: str = None,
        value: str = None,
        trait_id: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'trait'
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.id: Optional[Key] = None
        # elements
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif name is not None and value is not None:
            self.name = Key(name)
            self.value = Key(value)
            if trait_id is not None:
                self.id = Key(trait_id)
        else:
            raise RequiredValueError(('name', 'value'))

    def __str__(self):
        return f"{self.name}: {self.value}"


class Flag(Trait):
    """An important mechanism for giving type information to an object.
    It can also be use for adding binary constraints.

    .. note:: Used by LIFT v0.13 (FieldWorks). Mentioned in specification but
        not defined; assumed to be equivalent to ``Trait``.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()


class Text(LIFTUtilsBase):
    """Contains textual data mixed with ``span`` elements only.
    """

    def __init__(
        self,
        text: str = None,
        xml_tree: Optional[etree._Element] = None,
        subinit=False
    ):
        super().__init__()
        self._xml_tag = 'text'
        # elements
        self.pcdata = None
        self.span_items: Optional[List[Span]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._update_from_xml(xml_tree)
        elif text is not None:
            self.pcdata = PCData(text)
        else:
            raise RequiredValueError(('text',))

    def __str__(self):
        if self.span_items:
            s = f"{str(self.pcdata)}{''.join(str(s) for s in self.span_items)}"
        else:
            s = str(self.pcdata)
        return s


class Form(LIFTUtilsBase):
    """A representation of a string in a particular language and script.
    This is specified by the ``lang`` attribute.
    """

    def __init__(
        self,
        lang: Lang = None,
        text: Text = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'form'
        # attributes
        self.lang: Lang = None
        # elements
        self.text: Text = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._update_from_xml(xml_tree)
        elif lang is not None and text is not None:
            self.lang = Lang(lang)
            self.text = Text(text=text)
        else:
            raise RequiredValueError(('lang', 'text'))

    def __str__(self):
        return str(self.text)


class URLRef(LIFTUtilsBase):
    """This is a URL with a caption.
    """

    def __init__(
        self,
        href: str = None,
        label: dict = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'urlref'
        # attributes
        self.href = None
        # elements
        self.label: Optional[Multitext] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif href is not None:
            self.href = URL(href)
            if label is not None:
                self.set_label(label)
        else:
            raise RequiredValueError(('href',))

    def set_label(self, label_dict):
        if not isinstance(label_dict, dict):
            raise RequiredValueError(('dict of {{lang: text}} pairs',))
        self.label = Multitext(label_dict)

    def __str__(self):
        return str(self.href)


class Multitext(Text):
    """Allows for different representations of the same information.
    It can be in a given language, or in multiple languages.
    """

    def __init__(
        self,
        form_dict: dict = None,
        # trait_dict: dict = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=False)
        # Multitext is only used as a super class for other classes, so it
        # doesn't have it's own XML tag.
        del self._xml_tag
        # elements
        self.form_items: Optional[List[Form]] = None
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            if xml_tree is False:
                return
            self._update_from_xml(xml_tree)
        elif form_dict is not None:
            self.set_form_items(form_dict)

    def __str__(self):
        s = 'multitext'
        if self.form_items:
            # self.form_items.sort()
            s = f"{self.form_items[0].text} ({self.form_items[0].lang})"
            ct = len(self.form_items)
            if ct > 1:
                s = f"{s} ({ct} forms)"
        return s

    def get_form_by_lang(self, lang):
        """Return first form item with matching ``lang`` attribute.

        :var str lang: Language code; e.g. "en".
        """
        for f in self.form_items:
            if f.lang == lang:
                return f

    def set_form_items(self, form_dict):
        self.form_items = []
        for lg, tx in form_dict.items():
            self.form_items.append(Form(lang=lg, text=tx))


class Gloss(Form):
    """A representation of a sense's gloss.
    It's given in a particular language and script as specified by the ``lang``
    attribute.
    """

    def __init__(
        self,
        lang: str = None,
        text: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__(xml_tree=False)
        self._xml_tag = 'gloss'
        # elements
        self.trait_items: Optional[List[Trait]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif lang is not None and text is not None:
            self.lang = Lang(lang)
            self.text = Text(text=text)
        else:
            raise RequiredValueError(('lang', 'text'))

    def __str__(self):
        return f"{self.text} ({self.lang})"

    def set_trait_items(self, trait_dict):
        self.trait_items = []
        for name, data in trait_dict.items():
            value = data.get('value')
            trait_id = data.get('trait_id')
            self.trait_items.append(
                Trait(name=name, value=value, trait_id=trait_id)
            )


class Annotation(Multitext):
    """Provides a mechanism for adding meta-information to almost any element.
    """

    def __init__(
        self,
        name: str = None,
        value: str = None,
        who: str = None,
        when: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'annotation'
        # attributes
        self.name: Key = None
        self.value: Key = None
        self.who: Optional[Key] = None
        self.when: Optional[DateTime] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif name is not None and value is not None:
            self.name = Key(name)
            self.value = Key(value)
            if who is not None:
                self.who = Key(who)
            if when is not None:
                self.when = DateTime(when)
        else:
            raise RequiredValueError(('name', 'value'))


class Field(Multitext):
    """A generalised element to allow an application to store information.
    It's for information in a LIFT file that isn't explicitly described in the
    LIFT standard.
    """

    def __init__(
        self,
        field_type: str = None,
        name: str = None,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        self._xml_tag = 'field'
        # attributes
        if config.LIFT_VERSION == '0.13':
            self.type: Key = None
        else:
            self.name: Key = None
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        if config.LIFT_VERSION == '0.13':
            # self.trait_items: Optional[List[Flag]] = None
            self.trait_items: Optional[List[Trait]] = None
            # NOTE: I think there must be a typo in the docs. I think the
            # 'form_items' class should be 'Form', which is already accounted
            # for in the subclassing of 'Multitext'.
            # self.form_items: Optional[List[Span]] = None
        else:
            self.trait_items: Optional[List[Trait]] = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)
        elif config.LIFT_VERSION == '0.13' and field_type is not None:
            self.type = Key(field_type)
        elif config.LIFT_VERSION == '0.15' and name is not None:
            self.name = Key(name)
        else:
            if config.LIFT_VERSION == '0.13':
                value = 'field_type'
            else:
                value = 'name'
            raise RequiredValueError((value,))


class Extensible(LIFTUtilsBase):
    """Used to provide certain extra information in a controlled way.

    :ivar Optional[DateTime] date_created: Contains a date/timestamp saying
        when the element was added to the dictionary.
    :ivar Optional[DateTime] date_modified: Contains a date/timestamp saying
        when the element was last changed.
    :ivar Optional[List[Field]] field_items: Holds extra textual information.
    :ivar Optional[List[Trait]] trait_items: Adds type or constraint
        information.
    :ivar Optional[List[Annotation]] annotation: Adds meta-information
        describing the element.
    """

    def __init__(
        self,
        xml_tree: Optional[etree._Element] = None
    ):
        super().__init__()
        # Extensible is only used as a super class for other classes, so it
        # doesn't need its own XML tag.
        self._xml_tag = None
        # attributes
        self.date_created: Optional[DateTime] = None
        self.date_modified: Optional[DateTime] = None
        # elements
        self.field_items: Optional[List[Field]] = None
        if config.LIFT_VERSION == '0.13':
            # TODO: Find definition of "Flag" in v0.13?
            # self.trait_items: Optional[List[Flag]] = None
            self.trait_items: Optional[List[Trait]] = None
        else:
            self.trait_items: Optional[List[Trait]] = None
        self.annotation_items: Optional[List[Annotation]] = None

        if xml_tree is not None:
            self._update_from_xml(xml_tree)

    def add_annotation(self, name=None, value=None, who=None, when=None):
        return self._add_list_item(
            'annotation_items',
            Annotation,
            name=name,
            value=value,
            who=who,
            when=when,
        )

    def add_field(self, name=None):
        if config.LIFT_VERSION == '0.13':
            kwargs = {'field_type': name}
        else:
            kwargs = {'name': name}
        return self._add_list_item('field_items', Field, **kwargs)

    def add_trait(self, name=None, value=None, trait_id=None):
        return self._add_list_item(
            'trait_items',
            Trait,
            name=name,
            value=value,
            trait_id=trait_id,
        )

    def _add_attribs_to_xml_tree(self, xml_tree):
        for attrib in self.props.attributes:
            a = attrib.name
            x = config.XML_NAMES.get(a, a)
            xml_tree.set(x, self.__dict__.get(a))
        return xml_tree

    def set_date_created(self):
        self.date_created = DateTime()

    def set_date_modified(self):
        self.date_modified = DateTime()


def get_properties(class_, lift_version):
    classes = (class_, *class_.__bases__)
    props = {}

    if not hasattr(class_, '__bases__'):
        print('This class has no bases:', class_)
        return props

    props['attributes'] = {}
    props['elements'] = {}
    if Span in classes:
        props['attributes']['lang'] = (Lang, False)
        props['attributes']['href'] = (URL, False)
        props['attributes']['class_'] = (str, False)
        props['elements']['pcdata'] = (PCData, True)
        props['elements']['tail'] = (PCData, False)
        props['elements']['span_items'] = (list, Span, False)
    if Trait in classes:
        props['attributes']['name'] = (Key, True)
        props['attributes']['value'] = (Key, True)
        props['attributes']['id'] = (Key, False)
        props['elements']['annotation_items'] = (list, Annotation, False)
    if Text in classes:
        props['elements']['pcdata'] = (PCData, True)
        props['elements']['span_items'] = (list, Span, False)
    if Form in classes:
        props['attributes']['lang'] = (Lang, True)
        props['elements']['text'] = (Text, True)
        props['elements']['annotation_items'] = (list, Annotation, False)
    if URLRef in classes:
        props['attributes']['href'] = (URL, True)
        props['elements']['label'] = (Multitext, False)
    if Multitext in classes:
        props['elements']['form_items'] = (list, Form, False)
        props['elements']['trait_items'] = (list, Trait, False)
    if Gloss in classes:
        props['elements']['trait_items'] = (list, Trait, False)
    if Annotation in classes:
        props['attributes']['name'] = (Key, True)
        props['attributes']['value'] = (Key, True)
        props['attributes']['who'] = (Key, False)
        props['attributes']['when'] = (DateTime, False)
    if Field in classes:
        props['attributes']['date_created'] = (DateTime, False)
        props['attributes']['date_modified'] = (DateTime, False)
        if lift_version == '0.13':
            props['attributes']['type'] = (Key, True)
            # NOTE: See note about 'form_items' in class definition for 'Field'
            # above.
            # props['elements']['form_items'] = (list, Span, False)
        else:
            props['attributes']['name'] = (Key, True)
        props['elements']['annotation_items'] = (list, Annotation, False)
        props['elements']['trait_items'] = (list, Trait, False)
    if Extensible in classes:
        props['attributes']['date_created'] = (DateTime, False)
        props['attributes']['date_modified'] = (DateTime, False)
        props['elements']['field_items'] = (list, Field, False)
        props['elements']['trait_items'] = (list, Trait, False)
        props['elements']['annotation_items'] = (list, Annotation, False)

    return props
