import re
from nltk.tokenize import word_tokenize
from nltk.parse.corenlp import CoreNLPDependencyParser, CoreNLPParser

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
        
        return self.get_tenses()

    def run_tests(self, active_clauses):
        combined_text = '. '.join(active_clauses)
        return self.check_grammar(combined_text)
