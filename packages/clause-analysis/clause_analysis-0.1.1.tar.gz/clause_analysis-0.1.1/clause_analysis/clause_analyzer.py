import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.parse.corenlp import CoreNLPDependencyParser, CoreNLPParser

class ClauseAnalyzer:
    def __init__(self, parser_url='http://localhost:9000'):
        self.dep_parser = CoreNLPDependencyParser(url=parser_url)
        self.pos_parser = CoreNLPParser(url=parser_url, tagtype='pos')
        self.active_clauses = []
        self.passive_clauses = []
        self.conjunctions_and_connectors = [
            "and", "but", "or", "nor", "for", "so", "yet",
            "after", "although", "as", "because", "before", "even if", "even though", 
            "if", "once", "provided that", "rather than", "since", 
            "so that", "than", "that", "though", "unless", "until", "when", "whenever", 
            "where", "whereas", "wherever", "whether", "while",
            "accordingly", "anyway", "besides", "certainly", "consequently", "finally", 
            "furthermore", "hence", "however", "indeed", "instead", "likewise", "meanwhile", 
            "moreover", "nevertheless", "next", "nonetheless", "otherwise", "similarly", "still", 
            "then", "therefore", "thus",
            "after", "before", "since", "until", "how", "by", "By", "simply", "to"
        ]
        self.basic_pattern = r'\b(' + '|'.join(map(re.escape, self.conjunctions_and_connectors)) + r')\b'
    
    def split_clauses(self, text):
        sentences = sent_tokenize(text)
        clauses = []
        for sentence in sentences:
            sub_clauses = re.split(r'[,]', sentence)
            for sub_clause in sub_clauses:
                temp_clauses = re.split(self.basic_pattern, sub_clause)
                combined_sub_clauses = []
                temp_clause = ""
                for i, temp_clause_part in enumerate(temp_clauses):
                    temp_clause_part = temp_clause_part.strip()
                    if temp_clause_part:
                        if re.match(self.basic_pattern, temp_clause_part):
                            if temp_clause:
                                combined_sub_clauses.append(temp_clause.strip())
                                temp_clause = ""
                            combined_sub_clauses.append(temp_clause_part)
                        else:
                            if i > 0 and re.match(self.basic_pattern, temp_clauses[i-1]):
                                combined_sub_clauses[-1] += " " + temp_clause_part
                            else:
                                if temp_clause:
                                    combined_sub_clauses.append(temp_clause.strip())
                                    temp_clause = ""
                                combined_sub_clauses.append(temp_clause_part)
                if temp_clause:
                    combined_sub_clauses.append(temp_clause.strip())
                
                combined_sub_clauses = [clause for clause in combined_sub_clauses if not clause.lower().startswith('to ')]
                
                clauses.extend(self.refine_clauses(combined_sub_clauses))
        return clauses
    
    def refine_clauses(self, clause_list):
        refined_clauses = []
        current_clause = ""
        for part in clause_list:
            tokens = word_tokenize(part)
            pos_tags = self.pos_parser.tag(tokens)
            if any(tag.startswith('VB') for _, tag in pos_tags):
                if current_clause:
                    refined_clauses.append(current_clause.strip())
                    current_clause = part
                else:
                    current_clause = part
            else:
                if current_clause:
                    current_clause += " " + part
                else:
                    current_clause = part
        if current_clause:
            refined_clauses.append(current_clause.strip())
        return refined_clauses
    
    def search_tense_aspects(self, clauses):
        for sentence in clauses:
            parse, = self.dep_parser.raw_parse(sentence)
            parses_list = list(parse.triples())
            is_passive = False

            for dep in parses_list:
                if 'aux:pass' in dep[1]:
                    is_passive = True
                    break

            if is_passive:
                self.passive_clauses.append(sentence)
            else:
                self.active_clauses.append(sentence)

    def analyze(self, text):
        self.active_clauses = []
        self.passive_clauses = []
        
        clauses = self.split_clauses(text)
        self.search_tense_aspects(clauses)
        
        return self.active_clauses, self.passive_clauses

    def remove_initial_conjunctions(self, clauses):
        pattern = r'^\b(' + '|'.join(map(re.escape, self.conjunctions_and_connectors)) + r')\b\s*'
        cleaned_clauses = [re.sub(pattern, '', clause) for clause in clauses]
        return cleaned_clauses
