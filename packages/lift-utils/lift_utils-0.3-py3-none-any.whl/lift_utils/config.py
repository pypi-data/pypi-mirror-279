"""Define runtime global variables."""
from lxml import etree


LIB_VERSION = '0.3'
LIFT_VERSION_FIELDWORKS = '0.13'  # used by FLEx 9.1
LIFT_VERSION_LATEST = '0.15'
LIFT_VERSION_DEFAULT = LIFT_VERSION_FIELDWORKS
LIFT_VERSION = None

MULTIPLE_ITEM_TAGS = (
    'abbrev', 'annotation', 'description', 'entry', 'etymology', 'example',
    'field', 'form', 'gloss', 'illustration', 'label', 'media', 'note',
    'pronunciation', 'range', 'range-element', 'relation', 'reversal',
    'sense', 'span', 'subsense', 'trait', 'translation', 'usage',
    'variant',
)

XML_NAMES = {
    # object attribute keys (L) and corresponding LIFT XML tags (R)
    'abbrev_items': 'abbrev',
    'annotation_items': 'annotation',
    'class_': 'class',
    'date_created': 'dateCreated',
    'date_deleted': 'dateDeleted',
    'date_modified': 'dateModified',
    'description_items': 'description',
    'entry_items': 'entry',
    'etymology_items': 'etymology',
    'example_items': 'example',
    'field_items': 'field',
    'form_items': 'form',
    'gloss_items': 'gloss',
    'grammatical_info': 'grammatical-info',
    'illustration_items': 'illustration',
    'label_items': 'label',
    'lexical_unit': 'lexical-unit',
    'media_items': 'media',
    'note_items': 'note',
    'option_range': 'option-range',
    'pcdata': 'text',
    'pronunciation_items': 'pronunciation',
    'prop_type': 'type',
    'range_element_items': 'range-element',
    'range_items': 'range',
    'relation_items': 'relation',
    'reversal_items': 'reversal',
    'sense_items': 'sense',
    'span_items': 'span',
    'subsense_items': 'subsense',
    'trait_items': 'trait',
    'translation_items': 'translation',
    'usage_items': 'usage',
    'variant_items': 'variant',
    'writing_system': 'writing-system',
}

XML_PARSER = etree.XMLParser(remove_blank_text=True)
