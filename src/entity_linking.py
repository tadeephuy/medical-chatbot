import re
from utils import read_file, save_data


# def refine_data(path):
#     entities = []
#     data = read_file(path)
#     for obj in data:
#         if obj['relation'] in ['symptom'] and obj['source'] in src:
#             if obj['target'] not in entities:
#                 e = obj['target'].replace('.','').strip()
#                 entities.append(e)
#                 another_e = re.search(r'\((.*?)\)', e)
#                 if another_e != None:
#                     entities.append(another_e.group(1))


# if __name__ == '__main__':
#     data = read_file('../cancer_data/final_kb.json')
    
#     refine_data(data)