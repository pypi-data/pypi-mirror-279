import unittest
from clause_analysis.clause_analyzer import ClauseAnalyzer

class TestClauseAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = ClauseAnalyzer()

    def test_split_clauses(self):
        text = "This is a test sentence, and it should be split correctly."
        clauses = self.analyzer.split_clauses(text)
        self.assertTrue(len(clauses) > 1)

    def test_analyze(self):
        text = "The ball was thrown by the player. The player threw the ball."
        active, passive = self.analyzer.analyze(text)
        self.assertEqual(len(active), 1)
        self.assertEqual(len(passive), 1)

if __name__ == '__main__':
    unittest.main()
