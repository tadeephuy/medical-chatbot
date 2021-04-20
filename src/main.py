import argparse
import json

from utils import read_file,save_data


class Mapper:
    def __init__(self, data_path):
        self.data = read_file(data_path)

    def query(self, intent, entities):
        '''
        Query entities from KB 
        Input:
            intent: list 
                relation between 2 entities
            entities: list
                name belong with intent
        Output:
            list of related entites object
            { 
                'entity':
                'answer':
                'original_text':
            }
        '''
        final_answer = []
        for ent in entities:
            tmp_ans = []
            for sample in self.data:
                if intent == sample['relation']:
                    if ent == sample['source']:
                        # final_answer.append({
                        item = {
                            'entity': ent,
                            'answer': sample['target'],
                            'original_text': sample['original_text']
                        }
                        if item not in tmp_ans:
                            tmp_ans.append(item)
                    elif ent == sample['target']:
                        item = {
                            'entity': ent,
                            'answer': sample['source'],
                            'original_text': sample['original_text']
                        }
                        if item not in tmp_ans:
                            tmp_ans.append(item)
            tmp_ans = tmp_ans[:3]
            final_answer.extend(tmp_ans)
        # Ranking/sorting answer

        return final_answer

    def get_semanitc_frame(self, intent, entities,path_out):
        """
            semantic of agent action as a dictionary:
            {
            "intent":<>,
            "inform_slots": <>,
            "request_slots": <>
            }

            type of "intent" field is string
            type of "inform_slots" field is list of string
            type of "request_slots" field is list of string
        """

        answers = self.query(intent, entities)

        agent_action = {}
        agent_action['intent'] = intent
        agent_action['inform_slots'] = entities
        agent_action['response'] = answers
        agent_action['request_slots'] = []

        print(f'Saving to {path_out}.json ...')        
        save_data(agent_action,f'{path_out}.json')

        return agent_action

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--q', type=bool,default=False,
                        help='request for query option')
    parser.add_argument('--s', type=bool,default=False,
                        help='request for semantic frame option')
    parser.add_argument('--path_out', type=str,default='semantic_frame_out',
                        help='path to save file')

    parser.add_argument('--i', type=str,
                        help='intent input')
    parser.add_argument('--e',nargs="*",help='list of entities',default=[])

    args = parser.parse_args()
    
    mapper = Mapper('../cancer_data/final_kb.json')
    # ans = mapper.query('symptom', ['thalassemia', 'ung thư gan', "buồn nôn"])
    
    assert args.q != args.s

    if args.q == True:
        
        ans = mapper.query(args.i, args.e)
        for a in ans:
            print(f"{a['entity']} : {a['answer']}")
    elif args.s == True:
        ans = mapper.get_semanitc_frame(args.i, args.e,args.path_out)
        

