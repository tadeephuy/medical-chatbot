import requests
import random
from intent_matching import matching
from helper.preprocess import PreProcess
from helper.edit_distance import Distance
from ds_extraction.vb_ahocorasick import Dictionary
from answer_search import AnswerSearcher
## output API model matching
## mess,matching_question,confidence,answer
## KB query 


pp = PreProcess()
my_dict = Dictionary()
searcher = AnswerSearcher()

def pipeline_intent_reg(message):
    mess_norm = pp.process(message)
    mess_trans = pp.translate_vi2en(mess_norm)

    ## CONSTANT 
    type_dist = 'token_set'
    threshold = 0.75
    url_sim_model = 'https://5fde941fd0ee.ngrok.io/mm/'
    top_k = 1
    list_type_model = ['lstm','bert','distilbert']
    # type_model = random.choice(list_type_model)
    type_model = 'lstm'

    ## PATTERN MATCHING
    dict_pm_reg = matching(mess_trans,threshold,1,type_dist)

    diseases, symptoms = my_dict.get_ner(mess_trans, mode='aho', correct=False)

    # print('disease,symptoms :',diseases,symptoms,mess_trans)
    # print('dict_pm_reg',dict_pm_reg)

    if len(dict_pm_reg['response']) > 0 and (diseases or symptoms):
        intents = [i[0] for i in dict_pm_reg['response']]
        entities = {
            'diseases': diseases,
            'symptoms': symptoms
        }
        final_answers = searcher.search_by_dataframe(intents, entities)
        # print('final_answers',final_answers)
        if final_answers:
        # print('final_answers_type',type(final_answers))
            # answers_trans = [pp.translate_vi2en(a, 'vi') for a in final_answers]
            answers_trans = final_answers
        else:
            # answers_trans = ['Xin lỗi tôi không hiểu ý bạn, mời bạn hỏi lại !']
            answers_trans = ["Sorry, I don't understand your question !"]
        answers_pieces = []
        for ans in answers_trans:
            ans_split = ans.split('.')
            for a in ans_split:
                answers_pieces.append(a)


        dict_pm_reg['message_origin'] = message
        dict_pm_reg['process_type'] = 'pattern_matching'
        # dict_pm_reg['answers'] = ' '.join([pp.translate_vi2en(a, 'vi') for a in final_answers])
        dict_pm_reg['answers'] = answers_pieces
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
        # print('response',resp_sim.status_code)
        if resp_sim.status_code == 200:
            resp_json = resp_sim.json()
            dict_sim_reg = {}
            dict_sim_reg['message_origin'] = message
            dict_sim_reg['message'] = resp_json['message']['question']
            answers_trans = [resp_json['response'][-1][-2]]
            answers_pieces = []
            for ans in answers_trans:
                ans_split = ans.split('.')
                for a in ans_split:
                    answers_pieces.append(a)

            dict_sim_reg['answers'] = answers_pieces

            dict_sim_reg['process_type'] = 'similarity_matching'
            return dict_sim_reg
        else:
            # print('respsonse',resp_sim.status_code)
            dict_sim_reg = {}
            dict_sim_reg['message'] = mess_trans
            dict_sim_reg['response'] = [tuple(['How to not get liver cancer?',random.randint(0,100)/100])]
            dict_sim_reg['answers'] = ['Xin lỗi tôi không hiểu ý bạn, mời bạn hỏi lại !']
            dict_sim_reg['message_origin'] = message
            dict_sim_reg['process_type'] = 'mockup'
            return dict_sim_reg

if __name__=='__main__':
    # messages = ['pertussis có những triệu chứng gì','pertussis có những trịu chứng gì']
    sys_testing = {}
    sys_testing['general'] = [
        "cho hỏi cách phòng tránh bệnh viêm phổi thế nào ạ", ## success
        "điều trị bệnh thiếu máu bằng cách nào", ## success
        "bác sĩ có thể định nghĩa giúp tôi bệnh đau nửa đầu là gì được không ?", ## success
        "triệu chứng của bệnh ung thư vú là gì ?", ## success
        "vì sao tôi bị suy hô hấp vậy ?" ## success
    ]

    sys_testing['stroke'] = [
        "dấu hiệu của đột quỵ là gì?",
        "các phương pháp để ngăn ngừa đột quỵ là gì?",
        "béo phì có nguy cơ đột quỵ không?",
        "bạn có thể cho tôi biết về bệnh cao huyết áp không?",
        "bệnh tiểu đường có liên quan gì đến đột quỵ?"
    ]
    # for mess in messages:
    for key in sys_testing.keys():
        cases = sys_testing[key]
        # print('-'*20)
        # print('Case testing: ',key)
        for mess in cases:
            print('>'*50)
            print("User's message: ",mess)
            semantic_frame = pipeline_intent_reg(mess)
            print('Semantic frame: ',str(semantic_frame))
            # print("Agent's response: ",semantic_frame['answers'])
