from nltk.tokenize import word_tokenize
from nltk.parse.corenlp import CoreNLPParser

class ActivePhraseExtractor:
    def __init__(self, parser_url='http://localhost:9000'):
        self.pos_parser = CoreNLPParser(url=parser_url, tagtype='pos')

    def extract_active_phrases_from_dict(self, tense_dict):
        active_phrases = {}
        for tense, sentences in tense_dict.items():
            active_phrases[tense] = []
            for sentence in sentences:
                words = word_tokenize(sentence)
                pos_tags = [tag for _, tag in self.pos_parser.tag(words)]
                phrase = self._find_active_phrase(words, pos_tags, tense)
                if phrase:
                    active_phrases[tense].append(phrase)
        return active_phrases

    def _find_active_phrase(self, words, pos_tags, tense):
        auxiliaries = {'is', 'am', 'are', 'was', 'were', 'has', 'have', 'had', 'will', 'shall', 'should', 'could', 'would', 'be', 'been', "'s", "'re", "'d", "'ll", "'m", "'ve"}
        verb_forms = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}

        def extract_phrase_within_range(start_idx, end_idx):
            return ' '.join(words[start_idx:end_idx + 1])

        # Adjust the logic for each tense
        if tense == 'Future Perfect':
            for i, (word, tag) in enumerate(zip(words, pos_tags)):
                if word.lower() in {'will', "'ll", 'shall'}:
                    start_idx = i
                    for j in range(i + 1, len(words)):
                        if pos_tags[j] == 'VBN':
                            end_idx = j
                            return extract_phrase_within_range(start_idx, end_idx)

        if tense in {'Present Progressive', 'Past Progressive', 'Future Progressive', 
                     'Present Perfect Progressive', 'Past Perfect Progressive', 'Future Perfect Progressive'}:
            for i, (word, tag) in enumerate(zip(words, pos_tags)):
                if word.lower() in auxiliaries:
                    start_idx = i
                    for j in range(i + 1, len(words)):
                        if pos_tags[j] == 'VBG':
                            end_idx = j
                            return extract_phrase_within_range(start_idx, end_idx)

        for i, (word, tag) in enumerate(zip(words, pos_tags)):
            if word.lower() in auxiliaries:
                start_idx = i
                for j in range(i + 1, len(words)):
                    if pos_tags[j] in verb_forms:
                        end_idx = j
                        return extract_phrase_within_range(start_idx, end_idx)

        # Handle specific cases if no auxiliaries are found
        for i, (word, tag) in enumerate(zip(words, pos_tags)):
            if tense == 'Present Simple' and tag in {'VB', 'VBP', 'VBZ'}:
                return extract_phrase_within_range(i, i)
            elif tense == 'Past Simple' and tag == 'VBD':
                return extract_phrase_within_range(i, i)

        return None