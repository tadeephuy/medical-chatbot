"""
overview
symptoms
main_type
risk_factor
severe
prevention
diag
treatment
"""

"""
name,desc,prevent,cause,symptom,acompany,cure_department,cure_way

self.symptom_qwds = ['symptom', 'characterization', 'phenomenon']
self.cause_qwds = ['reason','cause']
self.acompany_qwds = ['complication', 'concurrent', 'occur','happen together', 'occur together', 'appear together', 'together', 'accompany', 'follow', 'coexist']
self.prevent_qwds = ['prevention', 'prevent', 'resist', 'guard', 'against','escape','avoid',
                     'how can I not', 
                     'how not to', 'why not', 'how to prevent']
self.lasttime_qwds = ['cycle', 'time','day','year','hour','days','years','hours','how long', 'how much time', 'a few days', 'how many years', 'how many days', 'how many hours', 'a few hours', 'a few years']
self.cureway_qwds = ['treat','heal','cure','how to treat', 'how to heal', 'how to cure', 'treatment', 'therapy']
self.cureprob_qwds = ['how big is the hope of cure', 'hope','probability', 'possibility', 'percentage', 'proportion']
self.easyget_qwds = ['susceptible population', 'susceptible','crowd','easy to infect', 'who', 'which people', 'infection', 'infect']
self.belong_qwds = ['what belongs to', 'belong', 'belongs','section','what section', 'department']
self.cure_qwds = ['what to treat', 'indication', 'what is the use', 'benefit', 'usefulness']
"""

dict_token_intent = {}

dict_token_intent['desc'] = ['information','define','what is']

dict_token_intent["symptom"] = ['symptom','expression','signal','symptoms','symptom','see','look','symptom','characterization','phenomenon']
dict_token_intent["cause"] = ['reason','cause','why']
dict_token_intent["acompany"] = ['complication','concurrent','occur','happen together','occur together','appear together','together','accompany','follow','coexist']
dict_token_intent["prevent"] = ['prevent','avoid','neither','anti','prevention method','preventing methods','prevention','prevent','resist','guard','against','escape','avoid',
                   'how can I not', 
                   'how not to','why not','how to prevent']
# dict_token_intent["lasttime"] = ['cycle','time','day','year','hour','days','years','hours','how long','how much time','a few days','how many years','how many days','how many hours','a few hours','a few years']
dict_token_intent["cure_way"] = ['treatment','rule','off','treatment','cure','over','cure','treatment','prick','what to treat','indication','what is the use','benefit','usefulness','treat','heal','cure','how to treat','how to heal','how to cure','treatment','therapy','how big is the hope of cure','hope','probability','possibility','percentage','proportion']

# dict_token_intent["cureprob"] = []
# dict_token_intent["risk_factor"] = ['risk','have susceptible','element','risk','potential','easy to meet','susceptible','susceptible population','susceptible','crowd','easy to infect','who','which people','infection','infect']
# dict_token_intent['diagnosis'] = ['diagnose','Diagnostic','check','guess','determined','test','accreditation','diag','screening','screening','filter']
# dict_token_intent['severe'] = ['danger','serious','level','affect','severity','injury','damages']
# dict_token_intent['main_type'] = ['variant','Category','species','include','including','types','type','including','types']
# dict_token_intent["belong"] = ['what belongs to','belong','belongs','section','what section','department']
# dict_token_intent["cure"] = []
