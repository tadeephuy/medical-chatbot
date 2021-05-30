import requests
from intent_matching import matching
from helper.preprocess import PreProcess
from helper.edit_distance import Distance
import random
## output API model matching
## mess,matching_question,confidence,answer
## KB query 


pp = PreProcess()

def pipeline_intent_reg(message):
    mess_norm = pp.process(message)
    mess_trans = pp.translate_vi2en(mess_norm)

    ## CONSTANT 
    type_dist = 'partial'
    threshold = 0.75
    url_sim_model = 'https://03629fbe8e48.ngrok.io/mm'
    top_k = 3
    list_type_model = ['lstm','bert','distilbert']
    # type_model = random.choice(list_type_model)
    type_model = 'lstm'

    ## PATTERN MATCHING
    dict_pm_reg = matching(mess_trans,threshold,type_dist)
    # print('dict_pm_reg',dict_pm_reg)
    if len(dict_pm_reg['response']) > 0:
        dict_pm_reg['message_origin'] = message
        dict_pm_reg['process_type'] = 'pattern_matching'
        return dict_pm_reg
    else:
        ## SIMILARITY SEARCH
        resp_sim = requests.post(url_sim_model,
                                    json={
                                        'question':mess_trans,
                                        'top_k': top_k,
                                        'model': type_model
                                        }
                                    )
        if resp_sim.status_code == 200:
            dict_sim_reg = resp_sim.json()
            dict_sim_reg['message_origin'] = message
            dict_sim_reg['process_type'] = 'similarity_matching'
            return dict_sim_reg
        else:
            # print('respsonse',resp_sim.status_code)
            dict_sim_reg = {}
            dict_sim_reg['message'] = mess_trans
            dict_sim_reg['response'] = [tuple(['How to not get liver cancer?',random.randint(0,100)/100])]
            dict_sim_reg['message_origin'] = message
            dict_sim_reg['process_type'] = 'mockup'
            return dict_sim_reg

if __name__=='__main__':
    messages = ['alo 1234','ai dễ bị ung thư gan vậy ?', 'pertussis có những triệu chứng gì']
    for mess in messages:
        print(pipeline_intent_reg(mess))
