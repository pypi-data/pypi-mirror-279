from nltk.tokenize import word_tokenize
from nltk.parse.corenlp import CoreNLPParser
import re

class PassiveTenseClassifier:
    def __init__(self, parser_url='http://localhost:9000'):
        self.pos_parser = CoreNLPParser(url=parser_url, tagtype='pos')
        self.reset_lists()

    def reset_lists(self):
        self.pre_si_passive = []
        self.pa_si_passive = []
        self.pre_pro_passive = []
        self.pa_pro_passive = []
        self.pre_per_passive = []
        self.pa_per_passive = []
        self.fu_si_passive = []
        self.fu_pro_passive = []
        self.fu_per_passive = []
        self.fu_per_pro_passive = []
        self.pa_per_pro_passive = []
        self.pre_per_pro_passive = []

    def classify_passive_tense(self, clause):
        words = word_tokenize(clause)
        pos_tags = [tag for _, tag in self.pos_parser.tag(words)]

        if any(aux in words for aux in ('is', "'s", 'am', "'m", 'are', "'re", 'may', 'can', 'shall')):
            if 'being' in words:
                self.pre_pro_passive.append(clause)
            else:
                self.pre_si_passive.append(clause)
        elif any(aux in words for aux in ('was', 'were', 'might', 'should', 'cloud')):
            if 'being' in words:
                self.pa_pro_passive.append(clause)
            else:
                self.pa_si_passive.append(clause)
        elif any(aux in words for aux in ('has', 'have', "'ve")):
            if 'been' in words:
                if 'being' in words:
                    self.pre_per_pro_passive.append(clause)
                else:
                    self.pre_per_passive.append(clause)
        elif 'had' in words:
            if 'been' in words:
                if 'being' in words:
                    self.pa_per_pro_passive.append(clause)
                else:
                    self.pa_per_passive.append(clause)
        elif any(aux in words for aux in ('will', "'ll")):
            if 'have' in words and 'been' in words:
                if 'being' in words:
                    self.fu_per_pro_passive.append(clause)
                else:
                    self.fu_per_passive.append(clause)
            elif 'being' in words:
                self.fu_pro_passive.append(clause)
            else:
                self.fu_si_passive.append(clause)

    def clean_clauses(self, clauses):
        return [clause.strip("[]'") for clause in clauses]

    def check_passive_grammar(self, raw_text):
        self.reset_lists()

        sentences = re.split(r'[.!?]', raw_text)

        for sentence in sentences:
            clauses = re.split(r'[,:;]', sentence)

            for clause in clauses:
                clause = clause.strip()
                if not clause:
                    continue

                self.classify_passive_tense(clause)

        result = {
            'Present Simple Passive': self.clean_clauses(self.pre_si_passive),
            'Past Simple Passive': self.clean_clauses(self.pa_si_passive),
            'Present Progressive Passive': self.clean_clauses(self.pre_pro_passive),
            'Past Progressive Passive': self.clean_clauses(self.pa_pro_passive),
            'Present Perfect Passive': self.clean_clauses(self.pre_per_passive),
            'Past Perfect Passive': self.clean_clauses(self.pa_per_passive),
            'Future Simple Passive': self.clean_clauses(self.fu_si_passive),
            'Future Progressive Passive': self.clean_clauses(self.fu_pro_passive),
            'Future Perfect Passive': self.clean_clauses(self.fu_per_passive),
            'Future Perfect Progressive Passive': self.clean_clauses(self.fu_per_pro_passive),
            'Present Perfect Progressive Passive': self.clean_clauses(self.pre_per_pro_passive),
            'Past Perfect Progressive Passive': self.clean_clauses(self.pa_per_pro_passive)
        }

        result = {tense: clauses for tense, clauses in result.items() if clauses}

        return result
