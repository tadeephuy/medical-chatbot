import json
import re

def read_file(path):
    data = []
    with open(path,encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def ranking(li_of_ent):
    TODO
    pass

def save_data(data, file_out):
    file_out = open(file_out, 'w')
    
    for item in data:
        item_str = str(item).replace(r"'", r'"')
        file_out.write(item_str) 
        file_out.write('\n')
    
def refine_string(s):
    return ' '.join(s.split()).lower()

def refine_data(path,file_out):
    data = read_file(path)
    re_data = []
    for obj in data:
        new_obj = {
            'source' : refine_string(obj['source']),
            'relation' : refine_string(obj['relation']),
            'target' : refine_string(obj['target']),
            'original_text' : refine_string(obj['original_text'])
        }
        re_data.append(new_obj)
    save_data(re_data,file_out)

def get_entity_list(path,out_file='entities.txt',src=['ung thư gan']):
    entities = []
    data = read_file(path)
    for obj in data:
        if obj['relation'] in ['symptom'] and obj['source'] in src:
            if obj['target'] not in entities:
                e = obj['target'].replace('.','').strip()
                entities.append(e)
                another_e = re.search(r'\((.*?)\)', e)
                if another_e != None:
                    entities.append(another_e.group(1))

    textfile = open(out_file, "w")
    for element in entities:
        textfile.write(element + "\n")

if __name__ == '__main__':
    # refine_data('../cancer_data/database_vi.json','../cancer_data/final_kb.json')
    get_entity_list('../cancer_data/final_kb.json',out_file='thalas_ent.txt',src=['thalassemia'])
    get_entity_list('../cancer_data/final_kb.json',out_file='recancer_ent.txt',src=['ung thư trực tràng'])
    get_entity_list('../cancer_data/final_kb.json',out_file='licancer_ent.txt',src=['ung thư gan'])
    