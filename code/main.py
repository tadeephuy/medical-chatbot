from helper.preprocess import PreProcess
from helper.edit_distance import Distance
# from fuzzywuzzy import fuzz

# pp = PreProcess()

dist = Distance()

token_rule = 'điều trị'
sentence = 'cho hỏi cách điều tri bệnh ung thư gan là gì vậy'

# print('partial: ',)
print(dist.compare_word(token_rule,sentence,0.8))
# print('token: ',fuzz.token_set_ratio(pp.remove_accent(token_rule),pp.remove_accent(mess)))