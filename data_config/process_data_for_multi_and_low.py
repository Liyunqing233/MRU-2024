import os
import json
from common import *
import copy
# 定义存放JSON文件的目录
# 定义输出文件的路径
#output_file = '../Multi_test/test.json'

all_data = []
# 遍历目录中的所有JSON文件
task = "aste"
data = "laptop14"
sents = []
labels = []
with open("../ASTE_L14/train.txt", 'r', encoding='UTF-8') as fp:
    words, labels = [], []
    for line in fp:
        line = line.strip()
        if line != '':
            words, tuples = line.split('####')
            sents.append(words)
            labels.append(eval(tuples))

instance_list = []

for sent, label in zip(sents, labels):
    instance = {}
    if task in ['acos','asqp']:
        if data in ['rest14','rest15','rest16']:
            instance['instruction'] = instruction_for_cot.replace("##", ", ".join(rest_aspect_cate_list)).replace('@@', task)
        else:
            instance['instruction'] = instruction_for_cot.replace("##", ", ".join(laptop_aspect_cate_list)).replace('@@', task)
        for i in range(1, 8):
            instance['input'] = sent
            output = "[Template_{}] ".format(i)
            templates_choose = templates_full_data['template_{}'.format(i)][0]
            for l in label:
                a, c, s, o = l
                if a == "NULL" or a == "null":
                    a = "one"

                if o == "NULL" or o == "null":
                    o = "described above"
                temp = templates_choose.format(Aspect=a.strip(), Opinion=o.strip(),
                                               Sentiment=s.strip(), Category=c.strip())
                output = output + " [sep] " + temp
            instance['input'] = "[Template_{}] ".format(i) + instance['input']
            instance['output'] = output.strip()
            instance_list.append(copy.deepcopy(instance))

    elif task == 'aste':
        instance['instruction'] = instruction_for_cot_ASTE.replace('@@', task)
        for i in range(1, 8):
            instance['input'] = sent
            output = "[Template_{}] ".format(i)
            templates_choose = templates_full_data_ASTE['template_{}'.format(i)][0]

            for l in label:
                a, o, s = l
                if a == 'NULL' or a == "null":
                    a = "one"
                aspect = ""
                opinion = ""
                sentiment = ""
                for ind in a:
                    aspect += sent.split()[ind] + " "
                for ind in o:
                    opinion += sent.split()[ind] + " "

                if s == "POS":
                    sentiment = "positive"
                elif s == "NEU":
                    sentiment = "neutral"
                elif s == "NEG":
                    sentiment = "negative"
                temp = templates_choose.format(Aspect=aspect.strip(), Opinion=opinion.strip(),
                                               Sentiment=sentiment.strip())
                output = output + " [sep] " + temp
            instance['input'] = "[Template_{}] ".format(i) + instance['input']
            instance['output'] = output.strip()
            instance_list.append(copy.deepcopy(instance))


    elif task == 'tasd':
        if data in ['rest14','rest15','rest16']:
            instance['instruction'] = instruction_for_cot_TASD.replace("##", ", ".join(rest_aspect_cate_list)).replace('@@', task)
        else:
            instance['instruction'] = instruction_for_cot_TASD.replace("##", ", ".join(laptop_aspect_cate_list)).replace('@@', task)
        for i in range(1, 8):
            instance['input'] = sent
            output = "[Template_{}] ".format(i)
            templates_choose = templates_full_data_TASD['template_{}'.format(i)][0]

            for l in label:
                a, c, s = l
                if a == "NULL" or a == "null":
                    a = "one"
                temp = templates_choose.format(Aspect=a.strip(), Category=c.strip(),
                                               Sentiment=s.strip())
                output = output + " [sep] " + temp
            instance['input'] = "[Template_{}] ".format(i) + instance['input']
            instance['output'] = output.strip()
            instance_list.append(copy.deepcopy(instance))

ratio = 0.02
output_path = '{}_{}_{}_train_plus.json'.format(task,data,ratio)
json.dump(instance_list[-int(len(instance_list)*ratio):], open(output_path, 'w'), ensure_ascii=False, indent=4)

