"""Define the basic datatypes."""

import uuid
from typing import List

from .utils import get_current_timestamp


class PCData(str):
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)


class DateTime(str):
    # format (str): YYYY-MM-DDTHH:MM:SSZZZZZZ
    # ZZZZZZ: +/-, H, H, :, M, M (offset from GMT)
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)
        else:
            return get_current_timestamp()


class Key(str):
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)


class Lang(str):
    # format (str): ISO[-SCRIPT[-x-PRIVATE]]
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)


class RefId(str):
    # format (HEX GUID): xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)
        else:  # generate new UUID
            return super().__new__(cls, str(uuid.uuid4()))


class URL(str):
    def __new__(cls, text=None):
        if text is not None:
            return super().__new__(cls, text)


class Prop:
    def __init__(
        self,
        name: str = None,
        required: bool = False,
        prop_type=None,
        item_type=None,
    ):
        self.name = name
        self.required = required
        self.prop_type = prop_type
        self.item_type = item_type


class Props:
    def __init__(
        self,
        attributes: List[Prop] = None,
        elements: List[Prop] = None,
    ):
        self.attributes = attributes
        self.elements = elements

    def add_to(self, prop_group_name, prop_obj):
        if prop_group_name == 'attributes':
            prop_group = self.attributes
            prop_group_names = (p.name for p in self.attributes)
        elif prop_group_name == 'elements':
            prop_group = self.elements
            prop_group_names = (p.name for p in self.elements)
        if prop_obj.name not in prop_group_names:
            prop_group.append(prop_obj)
