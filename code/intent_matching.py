from helper.preprocess import PreProcess
from helper.edit_distance import Distance
from config import INTENT_THRESHOLD

import json
import os

dist = Distance()
pp = PreProcess()

_PATH_DATA = '../data'
_PATH_TOKEN_INTENT = os.path.join(_PATH_DATA,'intent.json')

def matching(message):
    ## load json file

    dict_token_intent = json.load(open(_PATH_TOKEN_INTENT,'r'))
    ## get key token from dict_token_intent

    dict_result_matching = {}
    dict_result_matching['message'] = message
    

    list_intent = []
    list_token_match = []
    for item in list(dict_token_intent.keys()):
        ## TODO: DEFINE MATCHING ORDER
        ## init max probability

        max_prob = 0

        ## field: overview, disease, symptom, serverity, prevention, ... 
        field = dict_token_intent[item]
        tokens_rule = field['key']

        for token in tokens_rule:
            ## preprocess 
            token_norm = pp.process(token)
            mess_norm = pp.process(message)
            
            ## calculate edit distance with THRESHOLD in config.py
            dict_eval = dist.compare_word(token_norm,mess_norm)

            # dict_result_matching['confidence'] = dict_eval['partial']
            
            if dict_eval['partial'] >= INTENT_THRESHOLD and float(dict_eval['partial']) > max_prob:
                # dict_result_matching['intent'] = item
                # return dict_result_matching
                
                max_prob = float(dict_eval['partial'])
                # print('match',max_prob,token,message)
                tuple_match = (item,max_prob)
                if item not in [item[0] for item in list_intent]:
                    list_intent.append(tuple_match)
                    list_token_match.append(token_norm)
    dict_result_matching['intent'] = list_intent
    # dict_result_matching['max_prob'] = max_prob
    dict_result_matching['token'] = list_token_match
    dict_result_matching['message'] = message

    return dict_result_matching

if __name__ == '__main__':
    message = 'cho hỏi bệnh ung thư gan có điều trị hay diu tri được không vậy ?'
    print(matching(message))
