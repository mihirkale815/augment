from augment.data.instance import Instance,instance_gen,to_lines
import os
import sys
from collections import defaultdict
import random

def index_instances(instances):
    index = defaultdict(list)
    for instance in instances:
        for span_text,span_label in instance.spans:
            if span_label == 'O' : continue
            key = (span_label, instance.domain, instance.intent)
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
                #print(key,"not found in index")
                tgt_span_text = random.choice(tgt_index[key])
                new_spans.append([tgt_span_text, span_label])
                zero_new_spans = False
            else:
                new_spans.append([span_text, span_label])
    return new_spans,zero_new_spans

def create_augmented_dataset(instance_iterator,index,out_path):
    fout = open(out_path,"w")
    for instance in instance_iterator:
        new_spans,zero_new_spans = augment(instance,index)
        if zero_new_spans : "damn"
        new_span_text = " ".join([text for text, label in new_spans])
        span_text = " ".join([text for text, label in instance.spans])
        if len(new_spans) == 0 : continue
        #print(span_text," ==> ",new_span_text)
        fout.write("\n".join(to_lines(instance.domain,instance.intent,new_spans)) + "\n\n")


if __name__ == '__main__':

    data_dir = "data/multilingual_task_oriented_dialog_slotfilling"
    lang = "es"
    path_dict = defaultdict(dict)
    for lang in ['en','th']:
        path_dict[lang]['train'] = os.path.join(data_dir,lang,"train-{0}.conllu".format(lang))
        path_dict[lang]['dev'] = os.path.join(data_dir,lang,"train-{0}.conllu".format(lang))
        path_dict[lang]['test'] = os.path.join(data_dir,lang,"train-{0}.conllu".format(lang))



    igen = instance_gen(path_dict['en']['train'])
    a_instances = [instance for instance in igen]
    a_index = index_instances(a_instances)
    #print(len(index),sum([len(v) for v in index.values()]),len(instances),sum([len(instance.spans) for instance in instances]))

    igen = instance_gen(path_dict['th']['train'])
    b_instances = [instance for instance in igen]
    b_index = index_instances(b_instances)

    out_path = os.path.join(data_dir, "en", "train.syn.en.th.conllu")
    create_augmented_dataset(a_instances, b_index, out_path)
    out_path = os.path.join(data_dir, "th", "train.syn.th.en.conllu")
    create_augmented_dataset(b_instances, a_index, out_path)

    out_path = os.path.join(data_dir, "th", "train.syn.th.th.conllu")
    create_augmented_dataset(b_instances, b_index, out_path)

    #igen = instance_gen(out_path)
    #instances = [instance for instance in igen]
    #for instance in instances:
    #    print(instance.domain, instance.intent, instance.slot_labels, instance.tokens)

