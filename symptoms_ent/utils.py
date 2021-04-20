import json


def save_data(data, path):
    textfile = open(path, "w")
    for element in data:
        textfile.write(element)

def read_data(path):
    my_file = open(path, 'r')
    content_list = my_file.readlines()
    return content_list

def save_kb(data, file_out):
    file_out = open(file_out, 'w')
    
    for item in data:
        item_str = str(item).replace(r"'", r'"')
        file_out.write(item_str) 
        file_out.write('\n')
def sort_entites(path):
    data = read_data(path)
    data = list(set(data))
    save_data(data, path)

def read_kb(path):
    data = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def create_updated_kb(data, opt):
    '''
        Return a list of object
    '''
    res = []
    for sample in data:
        ss = {
            'source': refine_text(sample),
            'relation': 'symptom',
            'target': opt,
            'original_text': 'Empty'
        }
        if ss not in res:
            res.append(ss)

    return res

def update_kb(kb, new_kb, out_path):
    '''
        Merge and save KB
    '''
    print('Updating KB ...')
    kb.extend(new_kb)

    save_kb(kb,out_path)
    return kb


def refine_text(s):
    s = s.replace('.','').replace('\n','').strip()
    return s

def refine_kb(data,out_path):
    print('Refine final KB ... ')
    re_data= []
    for obj in data:
        src = {
            'source': refine_text(obj['source']),
            'relation': obj['relation'],
            'target': refine_text(obj['target']),
            'original_text' : refine_text(obj['original_text'])
        }
        re_data.append(src)
    
    save_kb(kb,out_path)
    
if __name__ == '__main__':
    # sort_entites('licancer_ent.txt')
    # sort_entites('recancer_ent.txt')
    # sort_entites('thalas_ent.txt')

    licancer = read_data('licancer_ent.txt')
    recancer = read_data('recancer_ent.txt')
    thalas = read_data('thalas_ent.txt')
    li_kb = create_updated_kb(licancer, 'ung thư gan')
    thalas_kb = create_updated_kb(thalas, 'thalassemia')
    re_kb = create_updated_kb(recancer, 'ung thư trực tràng')

    kb = read_kb('../cancer_data/final_kb.json')
    kb = update_kb(kb,li_kb,'../cancer_data/updated_kb.json')
    kb = update_kb(kb,thalas_kb,'../cancer_data/updated_kb.json')
    kb = update_kb(kb,re_kb,'../cancer_data/updated_kb.json')
    refine_kb(kb,'../cancer_data/final_kb.json')