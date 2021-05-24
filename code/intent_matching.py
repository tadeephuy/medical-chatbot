from helper.preprocess import PreProcess
from helper.edit_distance import Distance
from pattern_token import dict_token_intent
# from config import INTENT_THRESHOLD

import json
import os

dist = Distance()
pp = PreProcess()

_PATH_DATA = '../data'
_PATH_TOKEN_INTENT = os.path.join(_PATH_DATA,'intent.json')

"""
overview
symptom
prevent
treatment
risk_factor
diagnosis
severe
main_type
"""


def matching(message,INTENT_THRESHOLD,type_dist):
    """
    message: normalized, translated
    return: dictionary
        {   "message": <str>,
            "response": <tuple> (intent,confidence,token)
        }
    """
    ## load json file

    # dict_token_intent = json.load(open(_PATH_TOKEN_INTENT,'r'))
    ## get key token from dict_token_intent

    dict_result_matching = {}
    dict_result_matching['message'] = message
    

    list_intent = []
    list_token_match = []
    # mess_norm = pp.process(message)
    # mess_trans = pp.translate_vi2en(mess_norm)

    # print('message normalize',mess_norm)
    # print('message translate',mess_trans)
    for item in list(dict_token_intent.keys()):
        ## TODO: DEFINE MATCHING ORDER
        ## init max probability

        max_prob = 0

        ## field: overview, disease, symptom, serverity, prevention, ... 
        field = dict_token_intent[item]
        # tokens_rule = field['key']
        
        # print(item)
        for token in field:
            ## preprocess 
            
            # token_norm = pp.process(token)

            ## translate user's message from vi2en
            
            
            ## calculate edit distance with THRESHOLD in config.py
            dict_eval = dist.compare_word(token,message)

            if type_dist == 'partial':
                dist_ratio = dict_eval['partial']
            else:
                dist_ratio = dict_eval['token_set']
            # dict_result_matching['confidence'] = dict_eval['partial']
            
            if dist_ratio > INTENT_THRESHOLD and float(dist_ratio) > max_prob:
                # dict_result_matching['intent'] = item
                # return dict_result_matching
                
                max_prob = float(dist_ratio)
                # print('match',max_prob,token,message)
                tuple_match = (item,max_prob,token)
                if item not in [item[0] for item in list_intent]:
                    list_intent.append(tuple_match)
                    # list_token_match.append(token)
    # if list_intent:
    dict_result_matching['response'] = list_intent
    # else:
        # dict_result_matching['response'] = [('unk',1.0)]
    # dict_result_matching['max_prob'] = max_prob
    
    # dict_result_matching['token'] = list_token_match
    dict_result_matching['message'] = message

    return dict_result_matching

if __name__ == '__main__':
    ## TEST CASE
    messages = ['làm thế nào để không bị ung thư gan ?','ai dễ bị ung thư gan vậy ?']
    # print(matching(message))
    type_dist = 'partial'
    threshold = 0.7
    for mess in messages:
        mess_norm = pp.process(mess)
        mess_trans = pp.translate_vi2en(mess_norm)
        print(matching(mess_trans,threshold,type_dist))
