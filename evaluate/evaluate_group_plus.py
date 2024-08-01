# -*- coding: utf-8 -*-
import random
# This script handles the decoding functions and performance measurement

import re
import json
from  common import  *

def extract_spans_para(task, seq):
    quads = []
    sents = [s.strip() for s in seq.split('[sep]')][1:]
    templat = [s.strip() for s in seq.split('[sep]')][0]
    if task == 'asqp':
        for s in sents:
            #[sep] Noted for its fun, the ambience of the ambience general indicates a positive perspective. [sep] Noted for its great, the one of the restaurant prices indicates a positive perspective. [sep] Noted for its tasty, the food of the food quality indicates a positive perspective
            # Giving a neutral conclusion, the one related to the restaurant general seemed alright.
            # There's a resulting positive sentiment because the one in restaurant general is fair.
            try:
                aspect_pattern, opinion_pattern, entity_pattern, perspective_pattern = get_parser(templat)
                ot = re.findall(aspect_pattern, s)
                at = re.findall(opinion_pattern, s)
                ac = re.findall(entity_pattern, s)
                sp = re.findall(perspective_pattern, s)
            except :
                ac, at, sp, ot = '', '', '', ''

            quads.append((ac, at, sp, ot))
    else:
        raise NotImplementedError
    return quads


def compute_f1_scores(pred_pt, gold_pt):
    """
    Function to compute F1 scores with pred and gold quads
    The input needs to be already processed
    """
    # number of true postive, gold standard, predictions
    n_tp, n_gold, n_pred = 0, 0, 0

    for i in range(len(pred_pt)):
        n_gold += len(gold_pt[i])
        n_pred += len(pred_pt[i])

        for t in pred_pt[i]:
            if t in gold_pt[i]:
                n_tp += 1

    print(f"number of gold spans: {n_gold}, predicted spans: {n_pred}, hit: {n_tp}")
    precision = float(n_tp) / float(n_pred) if n_pred != 0 else 0
    recall = float(n_tp) / float(n_gold) if n_gold != 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision != 0 or recall != 0 else 0
    scores = {'precision': precision, 'recall': recall, 'f1': f1}

    return scores


def compute_scores(pred_seqs, gold_seqs, N):
    """
    Compute model performance
    """
    assert len(pred_seqs) == len(gold_seqs)
    num_samples = len(gold_seqs)

    all_labels, all_preds = [], []

    for i in range(num_samples):
        gold_list = extract_spans_para('asqp', gold_seqs[i])
        pred_list = extract_spans_para('asqp', pred_seqs[i])

        all_labels.append(gold_list)
        all_preds.append(pred_list)

    print("\nResults:")

    final_preds = []
    final_labels = []
    temp_pred = {}
    i = 0
    for pred, label in zip(all_preds, all_labels):
        if str(pred) in temp_pred:
            temp_pred[str(pred)] += 1
        else:
            temp_pred[str(pred)] = 1
        i += 1
        if i == 7:
            i = 0
            final = []

            for item in temp_pred:
                if temp_pred[item] > N:
                    final.extend(eval(item))
            if len(final) == 0:
                final = pred
            final_preds.append(final)
            final_labels.append(label)
            temp_pred = {}

    scores = compute_f1_scores(final_preds, final_labels)
    print(scores)

    return scores, all_labels, all_preds

outputs = []
targets = []
i = 0
inputs = []
inputs_all = []
with open('', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    data = [json.loads(line) for line in lines]
    for datass in data:
        outputs.append(datass['predict'])
        targets.append(datass['label'])


scores, all_labels, all_preds = compute_scores(outputs, targets, 2)
results = {'scores': scores, 'labels': all_labels, 'preds': all_preds}

