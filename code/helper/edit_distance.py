from fuzzywuzzy import fuzz
from helper.preprocess import PreProcess


class Distance:
    def __init__(self,preprocess):
        self.preprocess = PreProcess()

    def compare_word(self,token_rule,sentence,threshold):
        """
        compare 2 char

        params:
            character a, character b, threshold
        return:
            boolean, True if pass thresshold
        """
        partial_ratio = fuzz.partial_ratio(self.preprocess.remove_accent(token_rule),self.preprocess.remove_accent(sentence))
        token_set_ratio = fuzz.token_set_ratio(self.preprocess.remove_accent(token_rule),self.preprocess.remove_accent(sentence))

        partial_ratio = float(partial_ratio)/100
        token_set_ratio = float(token_set_ratio)/100
        
        if partial_ratio >= threshold and token_set_ratio >= threshold:
            return True
        else:
            return False