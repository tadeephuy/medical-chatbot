import json
from utils import read_file


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
                            'answer':sample['target'],
                            'original_text' : sample['original_text']
                        }
                        if item not in final_answer:
                            tmp_ans.append(item)
                    elif ent == sample['target']:
                        item = {
                            'entity': ent,
                            'answer':sample['source'],
                            'original_text' : sample['original_text']
                        }
                        if item not in final_answer:
                            tmp_ans.append(item)
            tmp_ans = tmp_ans[:3]
            final_answer.extend(tmp_ans)
        # Ranking/sorting answer 

        return final_answer


if __name__ == '__main__':
    mapper = Mapper('../cancer_data/final_kb.json')
    ans = mapper.query('symptom',['thalassemia','ung thư gan',"buồn nôn"])
    for a in ans:
        print(f"{a['entity']} : {a['answer']}")
    # print(ans)