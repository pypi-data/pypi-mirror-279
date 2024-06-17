import re
from nltk.tokenize import word_tokenize, sent_tokenize
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


class TenseAnalyzer:
    def __init__(self, parser_url='http://localhost:9000'):
        self.dep_parser = CoreNLPDependencyParser(url=parser_url)
        self.pos_parser = CoreNLPParser(url=parser_url, tagtype='pos')
        self.reset_lists()

    def reset_lists(self):
        self.fu_si, self.fu_gt, self.pre_per, self.pa_per, self.fu_per = [], [], [], [], []
        self.pre_pro, self.pa_pro, self.fu_pro, self.pre_part, self.pa_part, self.per_part, self.gerund = [], [], [], [], [], [], []
        self.pre_si, self.pa_si = [], []
        self.pre_per_pro, self.pa_per_pro, self.fu_per_pro, self.passive = [], [], [], []

    def search_tense_aspects(self, parsed_text, original_sentence):
        for parse in parsed_text:
            parses_list = list(parse.triples())
            added_verbs = set()
            sentence_start = 0

            for i in range(len(parses_list)):
                tag1 = parses_list[i][0][1]
                word1 = parses_list[i][0][0].lower()
                tag2 = parses_list[i][2][1]
                word2 = parses_list[i][2][0].lower()
                dep = parses_list[i][1]

                if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                    added_verbs = set()
                    sentence_start = i
                elif dep == 'parataxis':
                    continue
                elif dep == 'cop':
                    self.handle_copula(tag1, word1, tag2, word2, dep, original_sentence)
                elif dep == 'aux':
                    self.handle_aux(tag1, word1, tag2, word2, dep, parses_list, sentence_start, added_verbs, original_sentence)
                elif tag1 in ['VBZ', 'VBP']:
                    self.handle_present_simple(tag1, word1, parses_list, added_verbs, original_sentence)
                elif tag1 == 'VBD' and dep != 'aux':
                    self.handle_past_simple(tag1, word1, parses_list, sentence_start, i, added_verbs, original_sentence)

    def handle_copula(self, tag1, word1, tag2, word2, dep, original_sentence):
        if word2 in ('am', "'m", 'is', "'s", 'are', "'re"):
            self.pre_si.append(original_sentence)
        elif word2 in ('was', 'were'):
            self.pa_si.append(original_sentence)

    def handle_aux(self, tag1, word1, tag2, word2, dep, parses_list, sentence_start, added_verbs, original_sentence):
        if (tag1 in ('VB', 'JJ')) and (word2 in ('will', 'wo', "'ll")):
            self.fu_si.append(original_sentence)
        elif tag1 == 'VBG':
            self.handle_present_progressive_future(tag1, word1, word2, parses_list, sentence_start, original_sentence)
        elif tag1 == 'VBN':
            self.handle_past_participle(tag1, word1, word2, tag2, parses_list, sentence_start, original_sentence)
        elif word2 in ('can', 'shall'):
            self.pre_si.append(original_sentence)
        elif word2 in ('should', 'could'):
            self.pa_si.append(original_sentence)

    def handle_present_progressive_future(self, tag1, word1, word2, parses_list, sentence_start, original_sentence):
        not_identified = True
        if word2 in ('am', 'are', 'is', "'m", "'re"):
            if word1 == 'going':
                self.identify_going_to_future(word1, word2, parses_list, sentence_start, original_sentence)
            elif word1 == 'having':
                self.identify_perfect_participle(word1, word2, parses_list, sentence_start, original_sentence)
            if not_identified:
                self.pre_pro.append(original_sentence)
        elif word2 in ('was', 'were'):
            self.pa_pro.append(original_sentence)
        elif word2 in ('will', 'wo', "'ll"):
            self.identify_future_progressive(word1, word2, parses_list, sentence_start, original_sentence)
        elif word2 == 'been':
            self.identify_perfect_progressive(word1, word2, parses_list, sentence_start, original_sentence)

    def identify_going_to_future(self, word1, word2, parses_list, sentence_start, original_sentence):
        for j in range(sentence_start + 1, len(parses_list)):
            dep = parses_list[j][1]
            if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                break
            if dep == 'xcomp' and parses_list[j][2][1] == 'VB':
                self.fu_gt.append(original_sentence)
                return

    def identify_perfect_participle(self, word1, word2, parses_list, sentence_start, original_sentence):
        for j in range(sentence_start + 1, len(parses_list)):
            dep = parses_list[j][1]
            if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                break
            if dep == 'ccomp' and parses_list[j][2][1] == 'VBN':
                self.passive.append(original_sentence)
                return

    def identify_future_progressive(self, word1, word2, parses_list, sentence_start, original_sentence):
        for j in range(sentence_start + 1, len(parses_list)):
            dep = parses_list[j][1]
            if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                break
            if parses_list[j][2][0] == 'be' and parses_list[j][0][0] == word1:
                self.fu_pro.append(original_sentence)
                return

    def identify_perfect_progressive(self, word1, word2, parses_list, sentence_start, original_sentence):
        not_identified = True
        for j in range(sentence_start + 1, len(parses_list)):
            dep = parses_list[j][1]
            if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                break
            if parses_list[j][2][0] in ('have', 'has', "'ve"):
                for k in range(sentence_start + 1, len(parses_list)):
                    dep = parses_list[k][1]
                    if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                        break
                    if parses_list[k][2][0] in ('will', 'wo', "'ll"):
                        self.fu_per_pro.append(original_sentence)
                        not_identified = False
                        return
                if not_identified:
                    self.pre_per_pro.append(original_sentence)
                    not_identified = False
                    return
        if not_identified:
            self.pa_per_pro.append(original_sentence)

    def handle_past_participle(self, tag1, word1, word2, tag2, parses_list, sentence_start, original_sentence):
        if word2 == 'had':
            self.pa_per.append(original_sentence)
        elif word2 == 'has':
            self.pre_per.append(original_sentence)
        elif word2 in ('have', "'ve"):
            not_identified = True
            for j in range(sentence_start + 1, len(parses_list)):
                dep = parses_list[j][1]
                if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                    break
                if parses_list[j][2][0] in ('will', 'wo', "'ll"):
                    self.fu_per.append(original_sentence)
                    not_identified = False
                    return
            if not_identified:
                self.pre_per.append(original_sentence)
        elif tag2 == 'VBG':
            self.per_part.append(original_sentence)

    def handle_present_simple(self, tag1, word1, parses_list, added_verbs, original_sentence):
        is_present_simple = True
        has_aux = False

        for j in range(len(parses_list)):
            if parses_list[j][1] in ['aux', 'aux:pass'] and parses_list[j][2][0].lower() == word1:
                aux_verb = parses_list[j][0][0].lower()
                if aux_verb in ['will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might']:
                    is_present_simple = False
                    break
                if aux_verb in ['has', 'have', 'had', 'is', 'are', 'was', 'were', 'being', 'been']:
                    has_aux = True

        if has_aux and word1 not in added_verbs:
            for k in range(len(parses_list)):
                if parses_list[k][1] == 'aux' and parses_list[k][2][0].lower() == word1:
                    if parses_list[k][0][0].lower() in ['do', 'does']:
                        is_present_simple = True
                        break

        if is_present_simple and word1 not in added_verbs:
            self.pre_si.append(original_sentence)
            added_verbs.add(word1)

    def handle_past_simple(self, tag1, word1, parses_list, sentence_start, i, added_verbs, original_sentence):
        if word1 not in added_verbs:
            is_past_simple = True
            for j in range(sentence_start, i):
                if parses_list[j][1] in ['aux', 'aux:pass']:
                    is_past_simple = False
                    break
            if is_past_simple:
                self.pa_si.append(original_sentence)
                added_verbs.add(word1)

    def detect_specific_tenses(self, tokens, original_sentence):
        token_words = [word.lower() for word, pos in tokens]
        used_words = set()

        for i, word in enumerate(token_words):
            if word == 'will' and i + 2 < len(token_words) and token_words[i + 1] == 'have' and tokens[i + 2][1] == 'VBN':
                self.fu_per.append(original_sentence)
                used_words.update([i, i + 1, i + 2])

        for i, word in enumerate(token_words):
            if word in ('have', 'has', "'ve") and i + 1 < len(token_words) and tokens[i + 1][1] == 'VBN':
                if i not in used_words and (i + 1) not in used_words:
                    self.pre_per.append(original_sentence)
                    used_words.update([i, i + 1])

        for i, word in enumerate(token_words):
            if word == 'had' and i + 1 < len(token_words) and tokens[i + 1][1] == 'VBN':
                if i not in used_words and (i + 1) not in used_words:
                    self.pa_per.append(original_sentence)
                    used_words.update([i, i + 1])

        for i, word in enumerate(token_words):
            if word == 'will' and i + 1 < len(token_words) and tokens[i + 1][1].startswith('VB'):
                if i not in used_words and (i + 1) not in used_words:
                    self.fu_si.append(original_sentence)
                    used_words.update([i, i + 1])
            
            elif word in ('can', 'shall'):
                self.pre_si.append(original_sentence)
            elif word in ('should', 'could'):
                self.pa_si.append(original_sentence)

    def detect_simple_sentences(self, tokens, original_sentence):
        if len(tokens) == 2:
            word1, pos1 = tokens[0]
            word2, pos2 = tokens[1]

            if pos1 in ['PRP', 'NN', 'NNS', 'NNP', 'NNPS'] and pos2 in ['VBP', 'VBZ', 'VBD']:
                if pos2 == 'VBP':
                    self.pre_si.append(original_sentence)
                elif pos2 == 'VBZ':
                    self.pre_si.append(original_sentence)
                elif pos2 == 'VBD':
                    self.pa_si.append(original_sentence)

            if pos1 == 'EX' and pos2 in ['VBZ', 'VBP', 'VBD']:
                if pos2 == 'VBZ':
                    self.pre_si.append(original_sentence)
                elif pos2 == 'VBP':
                    self.pre_si.append(original_sentence)
                elif pos2 == 'VBD':
                    self.pa_si.append(original_sentence)

    def special_logic(self, tokens, original_sentence):
        if tokens[0][1] == 'VB':
            self.pre_si.append(original_sentence)

    def get_tenses(self):
        tenses = {
            'Present Simple': self.pre_si,
            'Past Simple': self.pa_si,
            'Present Progressive': self.pre_pro,
            'Present Perfect': self.pre_per,
            'Future Simple': self.fu_si,
            'Past Progressive': self.pa_pro,
            'Past Perfect': self.pa_per,
            'Present Perfect Progressive': self.pre_per_pro,
            'Past Perfect Progressive': self.pa_per_pro,
            'Future Progressive': self.fu_pro,
            'Future Perfect': self.fu_per,
            'Future Perfect Progressive': self.fu_per_pro,
        }
        return tenses

    def check_grammar(self, raw_text):
        self.reset_lists()

        sentences = re.split(r'[.!?]', raw_text)

        for sentence in sentences:
            clauses = re.split(r'[,:;]', sentence)

            for clause in clauses:
                clause = clause.strip()
                if not clause:
                    continue

                pos_text = self.pos_parser.tag(word_tokenize(clause))
                parsed_text = list(self.dep_parser.parse(word_tokenize(clause)))

                self.search_tense_aspects(parsed_text, clause)
                
                if not (self.fu_si or self.pre_per or self.pa_per or self.fu_per or self.pre_pro or self.pa_pro or self.fu_pro or self.pre_si or self.pa_si or self.pre_per_pro or self.pa_per_pro or self.fu_per_pro):
                    self.detect_specific_tenses(pos_text, clause)
                    self.detect_simple_sentences(pos_text, clause)
                    self.special_logic(pos_text, clause)
        
        return {tense: clauses for tense, clauses in self.get_tenses().items() if clauses}

    def run_tests(self, active_clauses):
        combined_text = '. '.join(active_clauses)
        return self.check_grammar(combined_text)

def print_non_empty_tenses(tenses):
    for tense, clauses in tenses.items():
        if len(clauses) > 0:
            print(f'{tense}: {clauses}')
