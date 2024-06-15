import unittest
from clause_analysis.passive_tense_classifier import PassiveTenseClassifier

class TestPassiveTenseClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = PassiveTenseClassifier()

    def test_classify_passive_tense(self):
        text = "The ball was being thrown by the player."
        result = self.classifier.check_passive_grammar(text)
        self.assertIn('Past Progressive Passive', result)

if __name__ == '__main__':
    unittest.main()
