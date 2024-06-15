import unittest
from lxml import etree

from . import DATA_PATH
from . import LEXICON

from lift_utils.utils import xmlfile_to_etree

LIFT_GOOD = DATA_PATH / "sango" / "sango.lift"


class TestParse(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON

    def test_lexicon_find_writing_systems(self):
        self.lexicon.vernacular_writing_systems.sort()
        self.lexicon.analysis_writing_systems.sort()
        self.assertEqual(
            self.lexicon.vernacular_writing_systems,
            ['sg', 'sg-fonipa']
        )
        self.assertEqual(
            self.lexicon.analysis_writing_systems,
            ['de', 'en', 'fr']
        )

    def test_lexicon_header_field_items(self):
        self.assertTrue(len(self.lexicon.header.fields.field_items) == 8)

    def test_lexicon_header_ranges(self):
        self.assertTrue(len(self.lexicon.header.ranges.range_items) == 20)

    def test_lexicon_entry_items(self):
        self.assertTrue(len(self.lexicon.entry_items) == 3507)

    def test_lexicon_get_item_from_id(self):
        refid = "ndâmbo kôlï/wâlï_fff4e6bb-9c09-43d6-ac11-b9220141b52b"
        item = self.lexicon.get_item_by_id(refid)
        self.assertIsNotNone(item)
        self.assertEqual(item.date_modified, "2023-04-20T19:31:03Z")

    def test_lexicon_get_parent_from_id(self):
        refid = "25222115-e109-4704-8e82-d7cd523c8cbd"
        parent = self.lexicon.get_item_parent_by_id(refid)
        self.assertIsNotNone(parent)
        self.assertEqual(parent.date_modified, "2023-04-20T19:31:03Z")


class TestReadWrite(unittest.TestCase):
    # NOTE: I haven't yet found a reliable way to compare XML file data. Using
    # "canonicalize" and "tostring" both result in XML strings whose child
    # element orders depend on the tree order rather than some kind of sorted
    # order useful for comparison. And since the element order of the input
    # file is unpredictable, there's no way to guarantee that the output file
    # will produce the same order, even if contents are identical.
    def test_read_write_file(self):
        infile = LIFT_GOOD
        outfile = DATA_PATH / "sango_out.lift"
        LEXICON.to_lift(outfile)
        xml_in = etree.tostring(
            xmlfile_to_etree(infile),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()
        xml_out = etree.tostring(
            xmlfile_to_etree(outfile),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()

        ranges_xml_in = etree.tostring(
            xmlfile_to_etree(infile.with_suffix('.lift-ranges')),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()
        ranges_xml_out = etree.tostring(
            xmlfile_to_etree(outfile.with_suffix('.lift-ranges')),
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True
        ).decode().rstrip()
        # xml_in = etree.canonicalize(
        #     xmlfile_to_etree(infile),
        #     strip_text=True
        # )
        # xml_out = etree.canonicalize(
        #     xmlfile_to_etree(outfile),
        #     strip_text=True
        # )
        # self.maxDiff = None
        # NOTE: In lieu of being able to compare xml content, just using a file
        # size comparison for the time being. This works okay as long as there
        # aren't too many comments in the infile, since comments aren't kept.
        # This tests that the outfile's size is within 7% of the infile's.
        delta = 0.05
        # print(len(xml_out)/len(xml_in))
        # print(len(ranges_xml_out)/len(ranges_xml_in))
        self.assertAlmostEqual(
            1,
            len(xml_out)/len(xml_in),
            delta=delta
        )
        self.assertAlmostEqual(
            1,
            len(ranges_xml_out)/len(ranges_xml_in),
            delta=delta
        )


class TestFind(unittest.TestCase):
    def setUp(self):
        self.lexicon = LEXICON

    def test_find_all_definition(self):
        self.assertEqual(
            len(self.lexicon.find_all(
                "husband",
                field="definition"
            )), 2)

    def test_find_all_gloss(self):
        self.assertEqual(len(self.lexicon.find_all("head")), 20)

    def test_find_all_grammatical_info(self):
        self.assertEqual(
            len(self.lexicon.find_all("Nom", field="grammatical-info")),
            2381
        )

    def test_find_all_header_field_contains(self):
        self.assertEqual(len(self.lexicon.find_all("1021", field="CAWL")), 1)

    def test_find_all_header_field_exact(self):
        self.assertEqual(len(self.lexicon.find_all(
            "1056",
            field="CAWL",
            match_type="exact"
        )), 1)

    def test_find_definition_contains(self):
        self.assertEqual(
            str(self.lexicon.find("man", field="definition").id),
            "f6c860ea-80ff-431a-a5dd-9469b315f40c"
        )

    def test_find_gloss_contains(self):
        self.assertEqual(
            str(self.lexicon.find("house").id),
            "086e06e3-a5f6-4c54-805a-4a1adcd51d4f"
        )

    def test_find_header_field_contains(self):
        self.assertEqual(
            str(self.lexicon.find("i-1056", field="CAWL").id),
            "25222115-e109-4704-8e82-d7cd523c8cbd"
        )

    def test_find_header_field_exact(self):
        self.assertIsNone(
            self.lexicon.find(
                "056",
                field="CAWL",
                match_type="exact"
            )
        )
