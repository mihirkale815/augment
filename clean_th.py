from collections import Counter
from augment.data.instance import Instance,instance_gen
import os
import sys
from collections import defaultdict
import random

base_data_dir = 'data/multilingual_task_oriented_dialog_slotfilling/'

def get_word_count(path):
    words = []
    for line in open(path):
        if line.startswith("# text:"):
            words.extend(line.lower().strip("\n").split(":")[1].strip().split())
    wc = Counter(words)
    return wc

def filter_dataset(instance_iterator,forbidden_words,out_path):
    fout = open(out_path, "w")
    instances = [instance for instance in instance_iterator]
    for instance in instances:
        tokens = set(instance.text.split())
        if len(forbidden_words.intersection(tokens)) > 0 : pass#print("skipping",instance.text)
        else :
            #print(instance.domain,instance.intent,instance.spans)
            fout.write("\n".join(instance.lines) + "\n\n")
    fout.close()




path = 'data/multilingual_task_oriented_dialog_slotfilling/{0}/train-{0}.conllu'
en_wc = get_word_count(path.format("en"))
th_wc = get_word_count(path.format("es"))
forbidden_words = {w:c for w,c in th_wc.items() if w in en_wc}
forbidden_word_set = set(forbidden_words.keys())
print(forbidden_words,len(forbidden_words),sum(forbidden_words.values()))

'''
filenames = [fn for fn in os.listdir(os.path.join(base_data_dir,"th")) if fn.endswith(".conllu")]
#filenames = ['train-th.conllu']
for filename in filenames:
    igen = instance_gen(os.path.join(base_data_dir,"th",filename))
    out_path = os.path.join(base_data_dir,"th_clean",filename)
    filter_dataset(igen,forbidden_word_set,out_path)
'''