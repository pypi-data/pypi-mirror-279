import unittest
from clause_analysis.tense_analyzer import TenseAnalyzer

class TestTenseAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TenseAnalyzer()

    def test_check_grammar(self):
        text = "The player will have been playing for an hour."
        result = self.analyzer.check_grammar(text)
        self.assertIn('Future Perfect Progressive', result)

if __name__ == '__main__':
    unittest.main()
