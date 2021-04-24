import re

from kb.balancer import Balancer
from tracker.tracker import Tracker
from inference import NLUprocess
from check_question import QuestionChecker
class Manager:
    def __init__(self):
        self.tracker = Tracker()
        self.balancer = Balancer() 
        self.NLUproc = NLUprocess("./phobert")
        self.question_classifier = QuestionChecker()

    def get_answer(self,user_mess,use_kb = False):        
        # 0 : is biz , 1 : is random : 2 : not intent
        '''
        tracker = Tracker()
        if question:
            a = is_random()
            b = is_biz()
            final_ans = get_final_answer(a,b)
            tracker.update()
            return final_ans
        else:
            return "not intent"
        '''
        # check question 
        user_mess = self.refine_input_string(user_mess)
        if self.question_classifier.is_question(user_mess):
            is_random_intent = self.question_classifier.is_random_intent(user_mess)
            if is_random_intent != "No Random":
                final_ans = {}
                final_ans['answer_entity'] = 'no match found'
                final_ans['entity'] = ''
                final_ans['intent'] = 'random intent'
                final_ans['original_text'] = is_random_intent
                return final_ans

            user_mess = user_mess.split(" ")

            result = self.NLUproc.inference([user_mess])
            
            if use_kb:
                result = result[0]
                final_ans = self.query_from_kb(user_mess,result)
                final_ans['intent'] = result['intent']
                self.tracker.update(final_ans['intent'],final_ans['entity'])
            else:
                final_ans = result
            # final_ans = self.get_final_answer(is_random_intent,final_ans)
            return final_ans
        else:
            # Not intent

            final_ans = {}
            final_ans['answer_entity'] = 'no match found'
            final_ans['entity'] = ''
            final_ans['intent'] = ''
            final_ans['original_text'] = 'Xin lỗi!\n Mình không hiểu những gì bạn nói. Mời bạn cung cấp lại thông tin giúp mình !'
            return final_ans

    def refine_input_string(self,s):
        s = s.lower().strip()
        s = re.sub('([.,!?()])', r' \1 ', s)
        s = re.sub('\s{2,}', ' ', s)
        s = s.strip()
        return s
    
    def query_from_kb(self,mess,result):
        '''
            Process single mess. Multi messages would be updated later.
        '''
        final_ans = {}

        entities = self.get_entities(mess,result['entities'])
        
        # TODO : Ranking system
        if result['intent'] == 'symptoms':
            result['intent'] = 'symptom'
        if result['intent'] == 'diag':
            result['intent'] = 'method_diagnosis'
        
        disease = self.tracker.get_prev_disease(entities)
     
        if disease == -1 or disease == []:
            final_ans['answer_entity'] = 'no match found'
            final_ans['entity'] = entities
            final_ans['intent'] = result['intent']
            final_ans['original_text'] = 'Xin lỗi!\n Mình không hiểu những gì bạn nói. Mời bạn cung cấp lại thông tin giúp mình !'
            return final_ans
        else:
            ans = self.balancer.query(disease,result['intent'], entities)
            # print(ans)
            if ans != -1 and ans != []:
                final_ans = ans[0]
                if type(final_ans['original_text'])==list:
                    final_ans['original_text'] = ' '.join(final_ans['original_text'])
                # final_ans = self.fill_empty_values(final_ans)
            else:
                final_ans['answer_entity'] = 'no match found'
                final_ans['entity'] = entities
                final_ans['intent'] = result['intent']
                final_ans['original_text'] = 'Xin lỗi!\n Mình không hiểu những gì bạn nói. Mời bạn cung cấp lại thông tin giúp mình !'

        return final_ans

    def get_entities(self,mess,preds):
        entities = []
        tmp = []
        for token,label in zip(mess,preds):
            # k = label.split()
            # print(k)
            if 'B' in label or 'I' in label:
                tmp.append(token)
            elif label=='O' and tmp != []:
                if len(tmp) > 1:
                    tmp= ' '.join(tmp)
                else:
                    tmp = tmp[0]
                entities.append(tmp)
                tmp = [] 
        if tmp != []:
            if len(tmp) > 1:
                tmp= ' '.join(tmp)
            else:
                tmp = tmp[0]
            entities.append(tmp)
            tmp = [] 
        return entities
       
    def get_final_answer(self,is_random_intent,final_ans):
        '''
            is_random_intent: str or -1
                str : is random intent
                -1 : not
            final_ans : dict    
        '''

        if is_random_intent == "No Random" and final_ans['intent'] == 'not intent':
            final_ans['intent'] = ''
            final_ans['original_text'] = 'Xin lỗi!\n Mình không hiểu những gì bạn nói. Mời bạn cung cấp lại thông tin giúp mình !'
        elif final_ans['intent'] == 'not intent':
            final_ans['intent'] = 'random intent'
            final_ans['original_text'] = is_random_intent
        
        return final_ans