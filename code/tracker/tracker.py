'''
Tracker for save history and tackle empty intent/entites/disease
'''
class Tracker:
    def __init__(self):
        self.history = []
        self.disease = ''
        self.intent = ''
        self.entities = []
        self.disease_list = self.read_disease('./tracker/diseases.txt')

    def update(self,intent,entities):

        self.disease = self.update_disease(entities)

        if intent != '':
            self.intent = intent
        if entities != []:
            self.entities = entities
        self.history.append({
            'intent': self.intent,
            'entities' : self.entities,
        })

    def get_prev_intent(self):
        return self.intent

    def get_prev_entities(self):
        return self.entities
    
    def get_prev_history(self):
        return self.history

    def get_prev_disease(self,entities):
        self.disease = self.update_disease(entities)
        return self.disease    
    
    def update_disease(self,entities):
        if entities == []:
            return self.disease
        for ent in entities:
            if ent in self.disease_list:
                self.disease = ent
                return self.disease
        return self.disease

    def read_disease(self,path):
        data = []
        with open(path,encoding='utf-8') as f:
            for line in f:
                data.append(line.replace('\n',''))
        return data

    def clear(self):
        self.history = []
        self.disease = ''
        self.intent = ''
        self.entities = []