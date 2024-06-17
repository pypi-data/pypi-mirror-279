import re

class ConjunctionsCleaner:
    def __init__(self):
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
    
    def remove_initial_conjunctions(self, clauses):
        pattern = r'^\b(' + '|'.join(map(re.escape, self.conjunctions_and_connectors)) + r')\b\s*'
        cleaned_clauses = [re.sub(pattern, '', clause) for clause in clauses]
        return cleaned_clauses
