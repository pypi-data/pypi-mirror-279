from nltk.tokenize import word_tokenize
from nltk.parse.corenlp import CoreNLPParser

class SubjectAdder:
    def __init__(self, parser_url='http://localhost:9000'):
        self.pos_parser = CoreNLPParser(url=parser_url, tagtype='pos')

    def add_subject_if_missing(self, clauses):
        updated_clauses = []
        starting_words = {'has', 'have', 'will', 'shall', 'can', 'could', 'would', 'is', 'am', 'are', 'was', 'were'}
        verb_forms = {'VB', 'VBD'}

        for clause in clauses:
            words = word_tokenize(clause.lower())
            pos_tags = [tag for _, tag in self.pos_parser.tag(words)]
            if (words[0] in starting_words) or (pos_tags[0] in verb_forms):
                updated_clause = "subject " + ' '.join(words)
            else:
                updated_clause = ' '.join(words)
                
            # Capitalize the first letter of the updated clause
            updated_clause = updated_clause.capitalize()
            updated_clauses.append(updated_clause)
                
        return updated_clauses