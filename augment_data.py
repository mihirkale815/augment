from augment.data.instance import Instance,BIODataUtils
import os
import sys
from collections import defaultdict
import random

def index_instances(instances,key_def='all'):
    index = defaultdict(list)
    for instance in instances:
        for span_text,span_label in instance.spans:
            if span_label == 'O' : continue
            key = (span_label, instance.domain, instance.intent)
            if key_def == 'slot': key = (span_label)
            index[key].append(span_text)
    return index

def augment(instance,tgt_index):
    new_spans = []
    zero_new_spans = True
    for span_text, span_label in instance.spans:
        if span_label == 'O' :
            new_spans.append([span_text,span_label])
        else:
            key = (span_label,instance.domain,instance.intent)
            if key in tgt_index :
                tgt_span_text = random.choice(tgt_index[key])
                new_spans.append([tgt_span_text, span_label])
                zero_new_spans = False
            else:
                new_spans.append([span_text, span_label])
    return new_spans,zero_new_spans

def create_augmented_dataset(instance_iterator,index,out_path,K=1):
    fout = open(out_path,"w")
    for instance in instance_iterator:
        for trial in range(0,K):
            new_spans,zero_new_spans = augment(instance,index)
            if zero_new_spans : "damn"
            new_span_text = " ".join([text for text, label in new_spans])
            span_text = " ".join([text for text, label in instance.spans])
            if len(new_spans) == 0 : continue
            #print(span_text," ==> ",new_span_text)
            fout.write("\n".join(BIODataUtils.to_lines(instance.domain,instance.intent,new_spans)) + "\n\n")
            #fout.write("\n".join(instance.lines) + "\n\n")
    fout.close()

def delexicalize(instance):
    text = []
    for span,slot in instance.spans:
        text.append(span if slot=='O' else slot)
    return " ".join(text)

def create_delexicalized_subset(instance_iterator,out_path):
    uniq_instance_templates = defaultdict(list)
    for instance in instance_iterator : uniq_instance_templates[delexicalize(instance)].append(instance)
    instances = [random.choice(vals) for vals in uniq_instance_templates.values()]
    fout = open(out_path, "w")
    print(len(uniq_instance_templates))
    #for key in uniq_instance_templates : print(key)
    for instance in instances:
        fout.write("\n".join(to_lines(instance.domain, instance.intent, instance.spans)) + "\n\n")
    fout.close()

def create_subset(instance_iterator,out_path,num_samples):
    fout = open(out_path, "w")
    instances = [instance for instance in instance_iterator]
    indices = [i for i in range(0,len(instances))]
    random.shuffle(indices)
    instances = [instances[i] for i in indices[:num_samples]]
    for instance in instances:
        #fout.write("\n".join(to_lines(instance.domain, instance.intent, instance.spans)) + "\n\n")
        fout.write("\n".join(instance.lines) + "\n\n")
    fout.close()

if __name__ == '__main__':

    data_dir = "data/multilingual_atis/"
    path_dict = defaultdict(dict)
    for lang in ['en', 'hi', 'tr']:
        path_dict[lang]['train'] = os.path.join(data_dir,lang,"train.bio")
        path_dict[lang]['dev'] = os.path.join(data_dir,lang,"dev.bio")
        path_dict[lang]['test'] = os.path.join(data_dir,lang,"test.bio")


    a_lang = 'en'
    b_lang = 'tr'

    instance_gen = BIODataUtils.instance_gen

    igen = instance_gen(path_dict[a_lang]['train'])
    a_instances = [instance for instance in igen]
    a_index = index_instances(a_instances)
    #print(len(index),sum([len(v) for v in index.values()]),len(instances),sum([len(instance.spans) for instance in instances]))

    igen = instance_gen(path_dict[b_lang]['train'])
    b_instances = [instance for instance in igen]
    b_index = index_instances(b_instances)

    #out_path = os.path.join(data_dir, "en", "train-en500.conllu")
    #create_subset(b_instances, out_path, 500)

    out_path = os.path.join(data_dir, a_lang, "train.syn.{a}.{b}.bio".format(a=a_lang,b=b_lang))
    create_augmented_dataset(a_instances, b_index, out_path)

    out_path = os.path.join(data_dir, b_lang, "train.syn.{b}.{a}.bio".format(a=a_lang,b=b_lang))
    create_augmented_dataset(b_instances, a_index, out_path)

    out_path = os.path.join(data_dir, b_lang, "train.syn.{b}.{b}.1.bio".format(b=b_lang))
    create_augmented_dataset(b_instances, b_index, out_path)

    out_path = os.path.join(data_dir, b_lang, "train.syn.{b}.{b}.2.bio".format(b=b_lang))
    create_augmented_dataset(b_instances, b_index, out_path)

    out_path = os.path.join(data_dir, b_lang, "train.syn.{b}.{b}.3.bio".format(b=b_lang))
    create_augmented_dataset(b_instances, b_index, out_path)

    out_path = os.path.join(data_dir, b_lang, "train.syn.{b}.{b}.4.bio".format(b=b_lang))
    create_augmented_dataset(b_instances, b_index, out_path)






'''
    out_path = os.path.join(data_dir, "en", "train.en.delex.conllu")
    create_delexicalized_subset(a_instances, out_path)

    #igen = instance_gen(out_path)
    #instances = [instance for instance in igen]
    #for instance in instances:
    #    print(instance.domain, instance.intent, instance.slot_labels, instance.tokens)
'''
