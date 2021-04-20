import os
import logging
import argparse
from tqdm import tqdm, trange

import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler

from transformers import RobertaConfig, AutoTokenizer

from model.model import JointphoBERT
from dataset import convert_input_file_to_tensor_dataset

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

    def inference(self, lines):
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
                                    "prop": intent_preds_cof[i],
                                    "entities": slot_preds_list[i]
                                    })
        return result

