import unittest

from . import LEXICON

from lift_utils import lexicon
from lift_utils import base
from lift_utils import datatypes
from lift_utils import errors

FIRST_ENTRY = LEXICON.entry_items[0]
FIRST_ENTRY_LAST_MODIFIED = FIRST_ENTRY.date_modified
FIRST_SENSE = FIRST_ENTRY.sense_items[0]
FIRST_SENSE_LAST_MODIFIED = FIRST_SENSE.date_modified


class TestAddExtensibleItems(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON
        self.entry = self.lexicon.entry_items[0]

    def test_add_annotation(self):
        self.assertRaises(
            errors.RequiredValueError,
            self.entry.add_annotation,
            name='name'
            )
        idx = self.entry.add_annotation(name="test", value="test value")
        self.assertIsInstance(self.entry.annotation_items[0], base.Annotation)
        self.assertEqual(len(self.entry.annotation_items), 1)
        del self.entry.annotation_items[idx]

    def test_add_field(self):
        self.assertRaises(
            errors.RequiredValueError,
            self.entry.add_field
        )
        idx = self.entry.add_field(name="Test Field")
        self.assertIsInstance(self.entry.field_items[0], base.Field)
        self.assertEqual(self.entry.field_items[0].type, 'Test Field')
        del self.entry.field_items[idx]

    def test_add_trait(self):
        self.assertRaises(
            errors.RequiredValueError,
            self.entry.add_trait
        )
        idx = 0
        if self.entry.trait_items:
            idx = len(self.entry.trait_items)
        self.entry.add_trait(name="trait-name", value="trait-value")
        self.assertIsInstance(self.entry.trait_items[idx], base.Trait)
        self.assertEqual(self.entry.trait_items[idx].name, 'trait-name')
        self.assertEqual(self.entry.trait_items[idx].value, 'trait-value')
        del self.entry.trait_items[idx]


class TestCreateBaseItems(unittest.TestCase):
    def test_create_annotation_missing_info(self):
        self.assertRaises(errors.RequiredValueError, base.Annotation)
        self.assertRaises(
            errors.RequiredValueError,
            base.Annotation,
            name='test'
        )

    def test_create_annotation_optional(self):
        self.anno = base.Annotation(
            name='optional-name',
            value='optional-value',
            who='optional-person',
            when='optional-timestamp'
        )
        self.assertIsInstance(self.anno.who, datatypes.Key)
        self.assertIsInstance(self.anno.when, datatypes.DateTime)
        self.assertEqual(self.anno.who, 'optional-person')
        self.assertEqual(self.anno.when, 'optional-timestamp')

    def test_create_annotation_required(self):
        self.anno = base.Annotation(name='test', value="value")
        self.assertIsInstance(self.anno.name, datatypes.Key)
        self.assertIsInstance(self.anno.value, datatypes.Key)
        self.assertEqual(self.anno.name, 'test')
        self.assertEqual(self.anno.value, 'value')

    def test_create_annotation(self):
        self.assertRaises(errors.RequiredValueError, base.Annotation)
        self.assertRaises(
            errors.RequiredValueError,
            base.Annotation,
            name='test'
        )
        self.anno = base.Annotation(
            name='name',
            value='value',
            who='optional-person',
            when='optional-timestamp'
        )
        self.assertIsInstance(self.anno.name, datatypes.Key)
        self.assertIsInstance(self.anno.value, datatypes.Key)
        self.assertIsInstance(self.anno.who, datatypes.Key)
        self.assertIsInstance(self.anno.when, datatypes.DateTime)
        self.assertEqual(self.anno.name, 'name')
        self.assertEqual(self.anno.value, 'value')
        self.assertEqual(self.anno.who, 'optional-person')
        self.assertEqual(self.anno.when, 'optional-timestamp')

    def test_create_field(self):
        self.assertRaises(errors.RequiredValueError, base.Field)
        self.field = base.Field(
            field_type="test-field"
        )
        self.assertIsInstance(self.field.type, datatypes.Key)
        self.assertEqual(self.field.type, "test-field")

    def test_create_form(self):
        self.assertRaises(errors.RequiredValueError, base.Form)
        self.form = base.Form(
            lang="en",
            text="text"
        )
        self.assertIsInstance(self.form.lang, datatypes.Lang)
        self.assertIsInstance(self.form.text, base.Text)
        self.assertEqual(self.form.lang, "en")
        self.assertEqual(str(self.form.text), "text")

    def test_create_span(self):
        self.assertRaises(errors.RequiredValueError, base.Span)
        self.span = base.Span(
            text="this text",
            lang="en",
            href="https://example.com",
            span_class="bold",
            tail="tail text"
        )
        self.assertIsInstance(self.span.pcdata, datatypes.PCData)
        self.assertIsInstance(self.span.tail, datatypes.PCData)
        self.assertIsInstance(self.span.lang, datatypes.Lang)
        self.assertIsInstance(self.span.href, datatypes.URL)
        self.assertIsInstance(self.span.class_, str)
        self.assertEqual(self.span.pcdata, "this text")
        self.assertEqual(self.span.tail, "tail text")
        self.assertEqual(self.span.lang, "en")
        self.assertEqual(self.span.href, "https://example.com")
        self.assertEqual(self.span.class_, "bold")

    def test_create_text(self):
        self.assertRaises(errors.RequiredValueError, base.Text)
        self.text = base.Text(
            text="text"
        )
        self.assertIsInstance(self.text.pcdata, datatypes.PCData)
        self.assertEqual(self.text.pcdata, "text")

    def test_create_trait(self):
        self.assertRaises(errors.RequiredValueError, base.Trait)
        self.trait = base.Trait(
            name="name",
            value="value",
            trait_id="trait-id"
        )
        self.assertIsInstance(self.trait.name, datatypes.Key)
        self.assertIsInstance(self.trait.value, datatypes.Key)
        self.assertIsInstance(self.trait.id, datatypes.Key)
        self.assertEqual(self.trait.name, "name")
        self.assertEqual(self.trait.value, "value")
        self.assertEqual(self.trait.id, "trait-id")

    def test_create_urlref(self):
        self.assertRaises(errors.RequiredValueError, base.URLRef)
        self.url = base.URLRef(
            href="https://www.example.com"
        )
        self.assertIsInstance(self.url.href, datatypes.URL)
        self.assertEqual(self.url.href, "https://www.example.com")


class TestModifyLexiconItems(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON
        self.entry = FIRST_ENTRY
        self.sense = FIRST_SENSE
        self.entry_last_modified = FIRST_ENTRY_LAST_MODIFIED
        self.sense_last_modified = FIRST_SENSE_LAST_MODIFIED

    def test_entry_add_etymology(self):
        idx = self.entry.add_etymology()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(
            self.entry.etymology_items[idx],
            lexicon.Etymology
        )
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)
        del self.entry.etymology_items[idx]

    def test_entry_add_note(self):
        idx = self.entry.add_note()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(self.entry.note_items[idx], lexicon.Note)
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)
        del self.entry.note_items[idx]

    def test_entry_add_pronunciation(self):
        idx = self.entry.add_pronunciation()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(
            self.entry.pronunciation_items[idx],
            lexicon.Phonetic
        )
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)
        del self.entry.pronunciation_items[idx]

    def test_entry_add_relation(self):
        idx = self.entry.add_relation()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(self.entry.relation_items[idx], lexicon.Relation)
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)
        del self.entry.relation_items[idx]

    def test_entry_add_sense(self):
        idx = self.entry.add_sense()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(self.entry.sense_items[idx], lexicon.Sense)
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)
        del self.entry.sense_items[idx]

    def test_entry_add_variant(self):
        idx = self.entry.add_variant()
        self.assertIsInstance(idx, int)
        self.assertIsInstance(self.entry.variant_items[idx], lexicon.Variant)
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)
        del self.entry.variant_items[idx]

    def test_entry_set_lexical_unit(self):
        self.entry.set_lexical_unit(
            {'en': 'english text', 'sg': 'atëne ti sängö'}
        )
        self.assertEqual(len(self.entry.lexical_unit.form_items), 2)
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)

    def test_entry_set_pronunciation_item(self):
        entry_id = "rô_ff402c0b-4eb5-4df1-bd29-a1900aaf7567"
        entry = self.lexicon.get_item_by_id(entry_id)
        labels = {
            "en": "pronunciation recording",
            "fr": "enregistrement de prononciation",
        }
        entry.pronunciation_items[0].add_media(
            href="file:///home/user/pronunciation.wav",
            label=labels
        )
        media_item = entry.pronunciation_items[0].media_items[0]
        self.assertEqual(
            media_item.href,
            "file:///home/user/pronunciation.wav"
        )
        self.assertEqual(len(media_item.label.form_items), 2)
        for f in media_item.label.form_items:
            self.assertIn(f.lang, labels.keys())
            self.assertIn(str(f.text), labels.values())
        self.assertIsNotNone(self.entry.date_modified)
        self.assertNotEqual(self.entry.date_modified, self.entry_last_modified)

    def test_etymology_add_gloss_item(self):
        entry_id = "yongo_eafee046-6df9-4162-8c38-a2536713b69f"
        entry = self.lexicon.get_item_by_id(entry_id)
        entry.etymology_items[0].add_gloss("en", "English gloss")
        idx = len(entry.etymology_items[0].gloss_items) - 1
        gloss_item = entry.etymology_items[0].gloss_items[idx]
        self.assertEqual(gloss_item.lang, 'en')
        self.assertEqual(str(gloss_item.text), 'English gloss')
        del entry.etymology_items[0].gloss_items[idx]

    def test_lexicon_add_entry_item(self):
        len_before = len(self.lexicon.entry_items)
        self.lexicon.add_entry()
        len_after = len(self.lexicon.entry_items)
        idx = len_after - 1

        self.assertEqual(len_after - 1, len_before)
        self.assertIsNotNone(self.lexicon.entry_items[idx].id)
        self.assertIsNotNone(self.lexicon.entry_items[idx].date_created)
        del self.lexicon.entry_items[idx]

    def test_sense_add_example(self):
        idx = self.sense.add_example()
        self.assertEqual(len(self.sense.example_items), 1)
        self.assertIsInstance(self.sense.example_items[idx], lexicon.Example)
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
        del self.sense.example_items[idx]

    def test_sense_add_gloss(self):
        len_before = len(self.sense.gloss_items)
        idx = self.sense.add_gloss(lang='en', text="gloss text")
        len_after = len(self.sense.gloss_items)
        self.assertEqual(len_after - 1, len_before)
        self.assertIsInstance(self.sense.gloss_items[idx], base.Gloss)
        self.assertEqual(self.sense.gloss_items[idx].lang, 'en')
        self.assertEqual(str(self.sense.gloss_items[idx].text), 'gloss text')
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
        del self.sense.gloss_items[idx]

    def test_sense_add_illustration(self):
        href = "file:///home/user/image.png"
        idx = self.sense.add_illustration(href=href)
        self.assertEqual(len(self.sense.illustration_items), 1)
        self.assertIsInstance(self.sense.illustration_items[idx], base.URLRef)
        self.assertEqual(self.sense.illustration_items[idx].href, href)
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
        del self.sense.illustration_items[idx]

    def test_sense_add_note(self):
        len_before = len(self.sense.note_items)
        idx = self.sense.add_note()
        len_after = len(self.sense.note_items)
        self.assertEqual(len_after - 1, len_before)
        self.assertIsInstance(self.sense.note_items[idx], lexicon.Note)
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
        del self.sense.note_items[idx]

    def test_sense_add_relation(self):
        idx = self.sense.add_relation()
        self.assertEqual(len(self.sense.relation_items), 1)
        self.assertIsInstance(self.sense.relation_items[idx], lexicon.Relation)
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
        del self.sense.relation_items[idx]

    def test_sense_add_reversal(self):
        len_before = len(self.sense.reversal_items)
        idx = self.sense.add_reversal()
        len_after = len(self.sense.reversal_items)
        self.assertEqual(len_after - 1, len_before)
        self.assertIsInstance(self.sense.reversal_items[idx], lexicon.Reversal)
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
        del self.sense.reversal_items[idx]

    def test_sense_add_subsense(self):
        idx = self.sense.add_subsense()
        self.assertEqual(len(self.sense.subsense_items), 1)
        self.assertIsInstance(self.sense.subsense_items[idx], lexicon.Sense)
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
        del self.sense.subsense_items[idx]

    def test_sense_set_definition(self):
        self.sense.set_definition(
            {'en': 'english text', 'sg': 'atëne ti sängö'}
        )
        self.assertEqual(len(self.sense.definition.form_items), 2)
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)

    def test_sense_set_grammatical_info(self):
        self.sense.set_grammatical_info('Nom')
        self.assertEqual(str(self.sense.grammatical_info), 'Nom')
        self.assertIsNotNone(self.sense.date_modified)
        self.assertNotEqual(self.sense.date_modified, self.sense_last_modified)
