import os
import logging
import argparse
from tqdm import tqdm, trange

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler

from transformers import RobertaConfig, AutoTokenizer

from model.model import JointphoBERT
from dataset import convert_input_file_to_tensor_dataset

from kb.mapper import Mapper

def load_tokenizer():
    return AutoTokenizer.from_pretrained("vinai/phobert-base")

def get_intent_labels():
    return [label.strip() for label in open("intent_label.txt", 'r', encoding='utf-8')]

def get_slot_labels():
    return [label.strip() for label in open("slot_label.txt", 'r', encoding='utf-8')]

def get_args(arg_folder):
    return torch.load(os.path.join(arg_folder, 'training_args.bin'))

def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

class NLUprocess:
    def __init__(self, arg_folder):
        self.args = get_args(arg_folder)
        self.device = get_device()
        self.model = JointphoBERT.from_pretrained(self.args.model_dir,\
                                                    args=self.args,\
                                                    intent_label_lst=get_intent_labels(),\
                                                    slot_label_lst=get_slot_labels())
        self.model.to(self.device)
        self.model.eval()

        self.intent_label_lst = get_intent_labels()
        self.slot_label_lst = get_slot_labels()

        self.slot_label_map = {i: label for i, label in enumerate(self.slot_label_lst)}

        self.pad_token_label_id = self.args.ignore_index

        self.tokenizer = load_tokenizer()

        self.softmax = nn.Softmax()

        self.mapper = Mapper('./kb/database.json')    

    def inference(self, lines,use_kb=False):
        dataset = convert_input_file_to_tensor_dataset(lines,\
                                                        self.args,\
                                                        self.tokenizer,\
                                                        self.pad_token_label_id)
        sampler = SequentialSampler(dataset)
        data_loader = DataLoader(dataset, sampler=sampler, batch_size=32)

        all_slot_label_mask = None
        intent_preds = None
        slot_preds = None

        result = []

        for batch in tqdm(data_loader, desc="Predicting"):
            batch = tuple(t.to(self.device) for t in batch)
            with torch.no_grad():
                inputs = {"input_ids": batch[0],
                        "attention_mask": batch[1],
                        "intent_label_ids": None,
                        "slot_labels_ids": None}
                inputs["token_type_ids"] = batch[2]
                outputs = self.model(**inputs)
                _, (intent_logits, slot_logits) = outputs[:2]

                intent_preds_cof = intent_logits.detach().cpu().numpy()
                slot_preds = slot_logits.detach().cpu().numpy()

                all_slot_label_mask = batch[3].detach().cpu().numpy()

                intent_preds = np.argmax(intent_preds_cof, axis=1)
                

                slot_preds = np.argmax(slot_preds, axis=2)
                slot_preds_list = [[] for _ in range(slot_preds.shape[0])]

                for i in range(slot_preds.shape[0]):
                    for j in range(slot_preds.shape[1]):
                        if all_slot_label_mask[i, j] != self.pad_token_label_id:
                            slot_preds_list[i].append(self.slot_label_map[slot_preds[i][j]])
                
                for i in range(len(intent_preds)):
                    result.append({"intent": self.intent_label_lst[int(intent_preds[i])],
                                    "highest_prop": float(self.softmax(torch.from_numpy(intent_preds_cof[i]))[int(intent_preds[i])]),
                                    "prop": self.softmax(torch.from_numpy(intent_preds_cof[i])).cpu().detach().numpy(),
                                    "entities": slot_preds_list[i]
                                    })
        if use_kb:
            result = result[0]
            final_result = self.query_from_kb(lines,result)
            final_result['intent'] = result['intent']
            return final_result        
        return result

    def query_from_kb(self,mess,result):
        '''
            Process single mess. Multi messages would be updated later.
        '''
        entities = self.get_entities(mess[0],result['entities'])
        
        # TODO : Ranking system
        if result['intent'] == 'symptoms':
            result['intent'] = 'symptom'
        ans = self.mapper.query(result['intent'], entities)[0]

        return ans

    def get_entities(self,mess,preds):
        entities = []
        tmp = []
        for token,label in zip(mess,preds):
            # k = label.split()
            # print(k)
            if 'B' in label or 'I' in label:
                tmp.append(token)
            elif label=='O' and tmp != []:
                if len(tmp) > 1:
                    tmp= ' '.join(tmp)
                else:
                    tmp = tmp[0]
                entities.append(tmp)
                tmp = [] 
        if tmp != []:
            if len(tmp) > 1:
                tmp= ' '.join(tmp)
            else:
                tmp = tmp[0]
            entities.append(tmp)
            tmp = [] 
        return entities
       
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="./phobert", help="Path of model")
    parser.add_argument("--input_text", type=str, help="input", default='tao muốn biết thông tin về bệnh thalassemia .')

    args = parser.parse_args()

    NLUmodel = NLUprocess(args.model)

    lines = [args.input_text.split(" ")]

    results = NLUmodel.inference(lines)

    print(results)


