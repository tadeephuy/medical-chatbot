import os
import pandas as pd
from py2neo import Graph

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(WORK_DIR, "medical_knowledge_base.csv")

class AnswerSearcher:
    def __init__(self):
        self.num_limit = 20
        # load data and normalize list values
        self.knowledge_base = pd.read_csv(DATA_PATH)
        self.knowledge_base['symptom'] = self.knowledge_base['symptom'].apply(self.clean_list_values)
        self.knowledge_base['acompany'] = self.knowledge_base['acompany'].apply(self.clean_list_values)
        self.knowledge_base['cure_department'] = self.knowledge_base['cure_department'].apply(self.clean_list_values)
        self.knowledge_base['cure_way'] = self.knowledge_base['cure_way'].apply(self.clean_list_values)

    def search_by_dataframe(self, intents, entities):
        final_answers = []
        mention_diseases = self.knowledge_base[self.knowledge_base['name'].isin(entities['diseases'])]
        # get row if list symptoms contains any elements of entities['symptoms']
        mention_symptoms = self.knowledge_base[self.knowledge_base.apply(lambda x:  any(item in x['symptom'].split(',') for item in entities['symptoms']), axis=1)]

        for question_type in intents:
            final_answer = []
            if question_type == 'disease_symptom' and not mention_diseases.empty:
                desc = mention_diseases['symptom'].iloc[0]
                subject = mention_diseases['name'].iloc[0]
                final_answer = 'The symptoms of {0} include: {1}'.format(subject, desc)

            elif question_type == 'symptom_disease' and not mention_symptoms.empty and entities['symptoms']:
                desc = mention_symptoms['name'].values
                subject = entities['symptoms'][0]
                final_answer = 'Symptoms {0} may be infected with: {1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

            elif question_type == 'disease_cause' and not mention_diseases.empty:
                desc = mention_diseases['cause'].iloc[0]
                subject = mention_diseases['name'].iloc[0]
                final_answer = 'The possible causes of {0} are: {1}'.format(subject, desc)

            elif question_type == 'disease_prevent' and not mention_diseases.empty:
                desc = mention_diseases['prevent'].iloc[0]
                subject = mention_diseases['name'].iloc[0]
                final_answer = '{0} precautions include: {1}'.format(subject, desc)

            elif question_type == 'disease_cureway' and not mention_diseases.empty:
                desc = mention_diseases['cure_way'].iloc[0]
                subject = mention_diseases['name'].iloc[0]
                final_answer = '{0} can try the following treatments: {1}'.format(subject, desc)

            elif question_type == 'disease_desc' and not mention_diseases.empty:
                desc = mention_diseases['desc'].iloc[0]
                subject = mention_diseases['name'].iloc[0]
                final_answer = '{0}, familiar with: {1}'.format(subject, desc)

            elif question_type == 'disease_acompany' and not mention_diseases.empty:
                desc = mention_diseases['acompany'].iloc[0]
                subject = mention_diseases['name'].iloc[0]
                final_answer = '{0}, familiar with: {1}'.format(subject, desc)
            
            if final_answer:
                final_answers.append(final_answer)

        return final_answers

    def clean_list_values(self, list_):
        list_ = list_.replace('[','')
        list_ = list_.replace(']','')
        list_ = list_.replace("'",'')
        list_ = list_.replace(", ",',')
        list_ = list_.replace(" ,",',')
        return list_


if __name__ == '__main__':
    searcher = AnswerSearcher()
    # res_sql = [{'question_type': 'symptom_disease', 'sql': ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) return m.name, r.name, n.name"]}]
    intents = ['disease_symptom']
    entities = {
        'diseases': ['pneumonia'],
        'symptoms': []
    }
    print(searcher.search_by_dataframe(intents, entities))