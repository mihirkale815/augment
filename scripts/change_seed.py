import json
from _jsonnet import evaluate_file, evaluate_snippet

def get_paths():
    paths = []
    template = "training_configs/{lang}_master.{emb}.{domain}.jsonnet"
    for lang in ['es','th']:
        for emb in ['muse','bert']:
            for dom in ['alarm','reminder','weather']:
                paths.append(template.format(lang=lang,emb=emb,domain=dom))
    return paths

def get_ext_vars():
    vars = {}
    vars['TRAIN_DATA_PATH'] = ''
    vars['TEST_DATA_PATH'] = ''
    vars['DEV_DATA_PATH'] = ''
    return vars

def set_seeds(paths,seed=0):
    for path in paths:
        print(path)
        config = json.loads(evaluate_file(path,ext_vars=get_ext_vars()))
        config['random_seed'] = seed
        config['pytorch_seed'] = seed
        config['numpy_seed'] = seed
        #config['train_data_path'] =
        #config['test_data_path'] = 'std.extVar("TEST_DATA_PATH")'
        #config['validation_data_path'] = 'std.extVar("DEV_DATA_PATH")'
        #json.dump(config,open(path,"w"))
        string = json.dumps(config)
        fout = open(path, "w")
        fout.write("".join([k for k in string if k!="'"]))
        fout.close()

def set_seeds_hacky(paths,seed=0):
    for path in paths:
        print(path)
        lines = open(path).readlines()
        string = "".join(lines[:-1]) #+ '\n "random_seed" : 1 , \n "pytorch_seed" = {0} , \n "numpy_seed" = {0} \n  }'
        json.dump(string,open(path,"w"))

seed = 1
paths = get_paths()
#print(paths)
set_seeds(paths,seed)