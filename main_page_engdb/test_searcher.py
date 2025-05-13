# test_searcher.py
import os
import unittest
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.analysis import StemmingAnalyzer
from searcher import search_projects

class TestSearcher(unittest.TestCase):
    def setUp(self):
        # Create a temporary index directory
        self.index_dir = "test_indexdir"
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

        # Define schema and create index
        schema = Schema(
            projectID=ID(stored=True),
            acronym=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            objective=TEXT(stored=True, analyzer=StemmingAnalyzer())
        )
        ix = create_in(self.index_dir, schema)

        # Add sample documents
        writer = ix.writer()
        writer.add_document(
            projectID="1",
            acronym="AI",
            title="Artificial Intelligence",
            objective="Develop AI systems"
        )
        writer.add_document(
            projectID="2",
            acronym="ML",
            title="Machine Learning",
            objective="Advance ML techniques"
        )
        writer.add_document(
            projectID="3",
            acronym="OD",
            title="Object Detection",
            objective="Detect objects in images"
        )
        writer.commit()

    def tearDown(self):
        # Clean up the test index directory
        for file in os.listdir(self.index_dir):
            os.remove(os.path.join(self.index_dir, file))
        os.rmdir(self.index_dir)

    def test_search_projects(self):
        # Change directory to the test index directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Perform a search query for "detect"
        search_term = "detect"
        results = search_projects(search_term)

        # Assert that results are returned
        self.assertGreater(len(results), 0, "No results found for the search term")
        self.assertEqual(results[0]["projectID"], "3", "Incorrect projectID in search results")
        self.assertEqual(results[0]["title"], "Object Detection", "Incorrect title in search results")

if __name__ == "__main__":
    unittest.main()