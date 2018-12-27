from augment.data.instance import Instance,instance_gen,to_lines
import os
import sys
from collections import defaultdict
import random


def delexicalize(instance):
    text = []
    for span,slot in instance.spans:
        text.append(span if slot=='O' else slot)
    return " ".join(text)

def create_paraphrases(path):
    igen = instance_gen(path)
    a_instances = [instance for instance in igen]
    pps = defaultdict(list)
    for instance in a_instances:
        pps[(instance.domain, instance.intent, tuple(set(instance.slot_type_labels)))].append(delexicalize(instance))
    return pps


if __name__ == '__main__':

    data_dir = "data/multilingual_task_oriented_dialog_slotfilling"
    lang = "en"
    path_dict = defaultdict(dict)
    for lang in ['en']:
        path_dict[lang]['train'] = os.path.join(data_dir,lang,"train-{0}.conllu".format(lang))
        path_dict[lang]['dev'] = os.path.join(data_dir,lang,"train-{0}.conllu".format(lang))
        path_dict[lang]['test'] = os.path.join(data_dir,lang,"train-{0}.conllu".format(lang))



    a_lang = 'en'

    pps = create_paraphrases(path_dict[a_lang]['train'])

    keys = list(pps.keys())
    for i, val in enumerate(pps[keys[0]]): print(i, keys[0], val)

