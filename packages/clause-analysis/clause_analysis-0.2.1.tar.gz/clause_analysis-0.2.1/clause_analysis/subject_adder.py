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
                updated_clauses.append("subject " + ' '.join(words))
            else:
                updated_clauses.append(' '.join(words))
                
        return updated_clauses