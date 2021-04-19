import json
import pandas as pd

# thalassemia
data = json.load(open('data.json',))

def build_kb(data,opt='liver cancer',out_path='database'):
    
    data = data[opt]
    kb = []
    for k in data.keys():
        relation = k.replace('Object_', '')
        d = data[k]  # dict
        sample = d[relation]
        original_text = d['original_text']
        
        if len(sample) != len(original_text):
            if original_text == []:
                original_text = ['None'] * len(sample)
            else:
                original_text = [original_text[0]] * len(sample)
        if len(sample) != len(original_text):
            print(relation)
            print(opt)
            print(len(sample),len(original_text))
            exit()

        for src, desc in zip(sample, original_text):
            if relation == 'overview':
                sample1 = {
                    "source": opt,
                    'relation': relation,
                    'target': desc,
                    'original_text': desc
                }
                sample2 = {
                    "source": opt,
                    'relation': relation,
                    'target': desc,
                    'original_text': desc
                }
            else:
                sample1 = {
                    "source": opt,
                    'relation': relation,
                    'target': src,
                    'original_text': desc
                }
                sample2 = {
                    "source": src,
                    'relation': relation,
                    'target': opt,
                    'original_text': desc
                }
            kb.append(sample1)
            kb.append(sample2)

    print('Writing to file ... ')
    with open(f'{out_path}.json', 'w') as jsonfile:
        json.dump(kb, jsonfile)

    return kb

if __name__ == '__main__':
    final_kb = []
    final_kb.extend(build_kb(data,'liver cancer','liver_cancer'))
    final_kb.extend(build_kb(data,'rectal cancer','rectal_cancer'))
    file_out = open('database.json', 'w')
    for item in final_kb:
        item_str = str(item).replace(r"'", r'"')
        file_out.write(item_str) 
        file_out.write('\n')