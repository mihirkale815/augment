import json
import os
from collections import defaultdict
import numpy as np
from scipy import stats
import sys
sys.path.append("/Users/mihirkale.s/PycharmProjects/augment/")
from augment.data.instance import  BIODataUtils,FBDataUtils
import allennlp.data.dataset_readers.dataset_utils.span_utils as span_utils

SNIPS_DOMAINS = ['book_restaurant','play_music','add_to_playlist',
               'search_screening_event','search_creative_work',
               'get_weather','rate_book','th.alarm','th.reminder','th.weather']


test_f1_key = "test_f1-measure-overall"
dev_f1_key = "best_validation_f1-measure-overall"

def parse_conlleval_output(path):
    f = open(path)
    text = f.readlines()
    metrics = {}
    for line in text[2:]:
        #print(line,line.strip("\n").strip(" ").split(" "))
        elements = line.strip("\n").strip(" ").split(" ")
        elements = [el for el in elements if el!='']
        slot, _, prec, _, rec, _,f1, count = elements
        slot = slot.split(":")[0].lower()
        prec = float(prec.split("%")[0])
        rec = float(rec.split("%")[0])
        f1 = float(f1)
        count = int(count)
        metrics[slot] = np.array([prec,rec,f1]) #np.array([prec,rec,f1,count])
    return metrics

def get_averaged_metrics(paths):
    metrics_per_run = []
    for path in paths:
        metrics_per_run.append(parse_conlleval_output(path))
    averaged_metrics = {}
    slots = list(metrics_per_run[0].keys())
    for slot in slots:
        arr = np.vstack([ metrics[slot] for metrics in metrics_per_run] )
        mean = arr.mean(axis=0)
        std = arr.std(axis=0)
        averaged_metrics[slot] = (mean,std)
    return averaged_metrics


def prepare_results_for_analysis():
    exps = ['baseline','1x','2x','4x']
    all_metrics = {}
    template = "{dir}/{domain}.bert.{exp}.{run_id}.{ext}"
    for domain in SNIPS_DOMAINS:
        all_metrics[domain] = {}
        for exp in exps:
            all_metrics[domain][exp] = {}
            result_files = []
            for run_id in ['run1', 'run2', 'run3']:
                result_file = template.format(domain=domain, exp=exp, run_id=run_id, ext='res', dir='result')
                result_files.append(result_file)
                averaged_metrics = get_averaged_metrics(result_files)
                all_metrics[domain][exp] = averaged_metrics
    counts = get_phrase_counts()
    slot_counts = get_slot_counts()
    context_counts = get_context_counts()
    for domain in SNIPS_DOMAINS:
        for exp in exps:
            for slot in all_metrics[domain][exp]:
                prec,rec,f1 = all_metrics[domain][exp][slot][0]
                prec = round(prec,2)
                rec = round(rec, 2)
                f1 = round(f1, 2)
                print(domain,exp,slot,prec,rec,f1,counts[domain][slot],slot_counts[domain][slot],context_counts[domain][slot])

def get_phrase_counts():
    counts = {}
    for domain in SNIPS_DOMAINS:
        counts[domain] = defaultdict(int)
        path = "data/snips/{domain}/train.bio".format(domain=domain)
        f = open(path)
        for line in f:
            if line.strip("\n") == "":continue
            if domain.startswith("th."):
                if line.startswith("#"): continue
                index,word,domain_intent,tag = line.strip("\n").split("\t")
                tag = tag.lower()
            else:
                tag,word = line.strip("\n").split("\t")
            if tag.startswith("b-") :
                slot = tag.split("-")[1].lower()
                counts[domain][slot] += 1
        #print(domain,slot,counts[domain][slot])
        f.close()
    return counts

def get_slot_counts():
    counts = {}
    avg_lens = {}
    for domain in SNIPS_DOMAINS:
        counts[domain] = defaultdict(list)
        slot_tokens = defaultdict(list)
        lens = defaultdict(list)
        path = "data/snips/{domain}/train.bio".format(domain=domain)
        data_util = FBDataUtils() if domain.startswith("th.") else BIODataUtils()
        gen = data_util.instance_gen(path)
        for instance in gen:
            if domain.startswith("th.") and domain.split(".")[1] != instance.domain: continue
            spans = instance.spans
            for text,slot in spans:
                slot = slot.lower()
                if slot == 'o' : continue
                slot_tokens[slot].extend(text.split())

        for slot,tokens in slot_tokens.items():
            counts[domain][slot] = len(set((tokens)))
            #print(domain,slot,counts[domain][slot])
    return counts

def get_context_counts():
    counts = {}
    for domain in SNIPS_DOMAINS:
        counts[domain] = defaultdict(list)
        context_tokens = defaultdict(list)
        path = "data/snips/{domain}/train.bio".format(domain=domain)
        data_util = FBDataUtils() if domain.startswith("th.") else BIODataUtils()
        gen = data_util.instance_gen(path)
        for instance in gen:
            if domain.startswith("th.") and domain.split(".")[1] != instance.domain : continue
            spans = instance.spans
            for i,(text,slot) in enumerate(spans):
                slot = slot.lower()
                if slot == 'o' : continue
                if i>=1 :
                    prev_text,prev_slot = spans[i-1]
                    context_tokens[slot].extend(prev_text.split()[-2:])
                if i<len(spans)-1:
                    next_text, next_slot = spans[i - 1]
                    context_tokens[slot].extend(next_text.split()[:2])

        for slot,tokens in context_tokens.items():
            counts[domain][slot] = len(set((tokens)))
            #print(domain,slot,counts[domain][slot],set(tokens))
            #print("*************************************")
    return counts

def print_scheme_a():
    model_dir = "saved_models"
    for lang in ['es','th']:
        for emb in ['muse','bert']:
            for dom in ['alarm','reminder','weather']:
                path = "{lang}.{dom}.{emb}".format(lang=lang,emb=emb,dom=dom)
                metrics = json.load(open(os.path.join(model_dir,path,"metrics.json")))
                dev_f1 = metrics['best_validation_f1-measure-overall']
                test_f1 = metrics['test_f1-measure-overall']
                print("\t".join(list(map(str,[lang,dom,emb,0,dev_f1,test_f1]))))

                try:
                    path = "{lang}_{lang}.{dom}.{emb}".format(lang=lang,emb=emb,dom=dom)
                    metrics = json.load(open(os.path.join(model_dir, path, "metrics.json")))
                    dev_f1 = metrics['best_validation_f1-measure-overall']
                    test_f1 = metrics['test_f1-measure-overall']
                    print("\t".join(list(map(str, [lang, dom, emb, 1, dev_f1, test_f1]))))
                except Exception as e : print(path,"does not exist. skipping")


                for mul in [2,4]:
                    path = "{lang}_{lang}.{mul}.{dom}.{emb}".format(lang=lang,emb=emb,dom=dom,mul=str(mul))
                    metrics = json.load(open(os.path.join(model_dir, path, "metrics.json")))
                    dev_f1 = metrics['best_validation_f1-measure-overall']
                    test_f1 = metrics['test_f1-measure-overall']
                    print("\t".join(list(map(str, [lang, dom, emb, mul, dev_f1, test_f1]))))

def print_scheme_b(path):
    metrics = {}
    domains = []
    saved_models_dirs = ['saved_models/snips.prime.run1','saved_models/snips.prime.run2','saved_models/snips.prime.run3']
    for exp in ['baseline','1x','2x','4x']:
        for saved_models_dir in saved_models_dirs:
            for domain in domains:
                path = os.path.join(saved_models_dir,domain,exp,'metrics.json')
                key = "-".join([domain,exp])
                metrics[key] = json.load(open(path))

def print_metrics(saved_model_dir,domains,run_ids,emb,exps):
    metrics = defaultdict(list)
    for domain in domains:
        for run_id in run_ids:
            for exp in exps:

                path = os.path.join(saved_model_dir,run_id,domain,emb,exp,'metrics.json')
                key = "#".join([domain,exp])
                metrics[key].append(json.load(open(path)))


    num_runs = len(run_ids)

    for key in metrics:
        avg_test_f1 = np.round(100*np.mean([metrics[key][i][test_f1_key] for i in range(num_runs)]),decimals=2)
        avg_dev_f1 = np.round(100*np.mean([metrics[key][i][dev_f1_key] for i in range(num_runs)]),decimals=2)

        std_test_f1 = np.round(100*np.std([metrics[key][i][test_f1_key] for i in range(num_runs)]),decimals=2)
        std_dev_f1 = np.round(100*np.std([metrics[key][i][dev_f1_key] for i in range(num_runs)]),decimals=2)

#        domain, emb, exp = key.split("-")

        domain,exp = key.split("#")
        print(domain,exp,avg_dev_f1,std_dev_f1,avg_test_f1,std_test_f1)


    return metrics

def get_results():
    test_f1_key = "test_f1-measure-overall"
    dev_f1_key = "best_validation_f1-measure-overall"

    saved_model_dir = 'saved_models/'

    domains = ['book_restaurant','rate_book','search_screening_event','search_creative_work','get_weather',
               'add_to_playlist','play_music']
    run_ids = ['snips.bert.run1', 'snips.bert.run2', 'snips.bert.run3']
    #run_ids = ['snips.prime.run1', 'snips.prime.run2', 'snips.prime.run3']
    #run_ids = ['sim-m.run1','sim-m.run3','sim-m.run3','sim-m']
    emb = 'bert'
    exps = ['baseline', '1x', '2x', '4x']


    #domains = ['alarm','reminder','weather']
    #run_ids = ['th.run1', 'th.run2', 'th.run3']
    #exps = ['train-th','train.1x','train.2x','train.4x']
    #print_metrics(saved_model_dir, domains, run_ids, '',exps)
    #emb = ''
    #metrics = print_metrics(saved_model_dir, domains, run_ids, emb, exps)


    domains = ['alarm','reminder','weather']
    run_ids = ['xling/th','xling2/th','xling3/th']
    exps = ['train.xl_ours','train.xl_baseline']
    print_metrics(saved_model_dir, domains, run_ids, '',exps)
    emb = ''
    metrics = print_metrics(saved_model_dir, domains, run_ids, emb, exps)



    '''
    for domain in domains:
        key = "#".join([domain, 'baseline'])
        a = [metrics[key][i][test_f1_key] for i in range(len(run_ids))]
        for exp in exps:
            key = "#".join([domain, exp])
            b = [metrics[key][i][test_f1_key] for i in range(len(run_ids))]
            print(domain,exp,stats.ttest_ind(a+a, b+b, axis=0, equal_var=False, nan_policy='propagate'))
    '''



prepare_results_for_analysis()
#get_slot_counts()
#get_context_counts()


