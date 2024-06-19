from nltk.tokenize import word_tokenize
from nltk.parse.corenlp import CoreNLPParser

class PassivePhraseExtractor:
    def __init__(self, parser_url='http://localhost:9000'):
        self.pos_parser = CoreNLPParser(url=parser_url, tagtype='pos')

    def extract_passive_phrases_from_dict(self, tense_dict):
        passive_phrases = {}
        for tense, sentences in tense_dict.items():
            passive_phrases[tense] = []
            for sentence in sentences:
                words = word_tokenize(sentence)
                pos_tags = [tag for _, tag in self.pos_parser.tag(words)]
                phrase = self._find_passive_phrase(words, pos_tags)
                if phrase:
                    passive_phrases[tense].append(phrase)
        return passive_phrases

    def _find_passive_phrase(self, words, pos_tags):
        auxiliaries = {'is', 'am', 'are', 'was', 'were', 'has', 'have', 'had', 'will', 'would', 'been'}
        past_participles = {'VBN'}

        aux_index = -1
        vbn_index = -1

        for i, (word, tag) in enumerate(zip(words, pos_tags)):
            if word.lower() in auxiliaries and aux_index == -1:
                aux_index = i
            if tag in past_participles and aux_index != -1:
                vbn_index = i
                break

        if aux_index != -1 and vbn_index != -1:
            return ' '.join(words[aux_index:vbn_index+1])
        return None