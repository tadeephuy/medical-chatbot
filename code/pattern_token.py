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

dict_token_intent = {}

dict_token_intent['overview'] = ['information','define']

dict_token_intent["symptom"] = ['symptom','expression','signal','symptoms','symptom','see','look','symptom','characterization','phenomenon']
# dict_token_intent["cause"] = ['reason','cause']
# dict_token_intent["accompany"] = ['complication','concurrent','occur','happen together','occur together','appear together','together','accompany','follow','coexist']
dict_token_intent["prevent"] = ['prevent','avoid','neither','anti','prevention method','preventing methods','prevention','prevent','resist','guard','against','escape','avoid',
                   'how can I not', 
                   'how not to','why not','how to prevent']
# dict_token_intent["lasttime"] = ['cycle','time','day','year','hour','days','years','hours','how long','how much time','a few days','how many years','how many days','how many hours','a few hours','a few years']
dict_token_intent["treatment"] = ['treatment','rule','off','treatment','cure','over','cure','treatment','prick','what to treat','indication','what is the use','benefit','usefulness','treat','heal','cure','how to treat','how to heal','how to cure','treatment','therapy','how big is the hope of cure','hope','probability','possibility','percentage','proportion']
# dict_token_intent["cureprob"] = []
dict_token_intent["risk_factor"] = ['risk','have susceptible','element','risk','potential','easy to meet','susceptible','susceptible population','susceptible','crowd','easy to infect','who','which people','infection','infect']
dict_token_intent['diagnosis'] = ['diagnose','Diagnostic','check','guess','determined','test','accreditation','diag','screening','screening','filter']
dict_token_intent['severe'] = ['danger','serious','level','affect','severity','injury','damages']
dict_token_intent['main_type'] = ['variant','Category','species','include','including','types','type','including','types']
# dict_token_intent["belong"] = ['what belongs to','belong','belongs','section','what section','department']
# dict_token_intent["cure"] = []
