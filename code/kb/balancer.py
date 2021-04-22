from kb.mapper import Mapper

class Balancer:
    def __init__(self):
       
        self.thallas = Mapper('./kb/thalassemia.json')    
        self.liver = Mapper('./kb/ung_thư_gan.json') 
        self.rec = Mapper('./kb/ung_thư_trực_tràng.json')
    
    def query(self,disease,intent,entities):
        if disease == '':
            return -1
        if disease =='thalassemia':
            return self.thallas.query(intent,entities)
        elif disease =='ung thư gan':
            return self.liver.query(intent,entities)
        else:
            return self.rec.query(intent,entities)


    