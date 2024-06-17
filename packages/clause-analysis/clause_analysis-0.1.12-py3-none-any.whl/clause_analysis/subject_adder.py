from nltk.tokenize import word_tokenize
from nltk.parse.corenlp import CoreNLPParser

class SubjectAdder:
    def __init__(self, parser_url='http://localhost:9000'):
        self.pos_parser = CoreNLPParser(url=parser_url, tagtype='pos')

    def add_subject_if_missing(self, clauses):
        updated_clauses = []
        starting_words = {'VB', 'VBD', 'has', 'have', 'will', 'shall', 'can', 'could', 'would', 'is', 'am', 'are', 'was', 'were'}
        
        for clause in clauses:
            words = word_tokenize(clause)
            pos_tags = [tag for _, tag in self.pos_parser.tag(words)]
            if (words[0].lower() in starting_words) or (pos_tags[0] in {'VB', 'VBD'}):
                updated_clauses.append("Subject " + clause)
            else:
                updated_clauses.append(clause)
                
        return updated_clauses
