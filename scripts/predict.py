import json





def convert_to_conll_format(pred_file,output_file):
    fout = open(output_file,"w")
    fin = open(pred_file)
    for output in fin:
        output = json.loads(output)
        mask = output['mask']
        pred_tags = output['tags']
        gold_tags = output['gold_tags']
        words = output['words']
        pred_tags = [tag for i,tag in enumerate(pred_tags) if mask[i]==1]
        gold_tags = [tag for i, tag in enumerate(gold_tags) if mask[i] == 1]
        words = [tag for i, tag in enumerate(words) if mask[i] == 1]

        for word,pred,gold in zip(words,pred_tags,gold_tags):
            fout.write(" ".join([word,gold.upper(),pred.upper()]) + "\n")
        fout.write("\n")

SNIPS_DOMAINS = ['book_restaurant','play_music','add_to_playlist',
               'search_screening_event','search_creative_work',
               'get_weather','rate_book','th.alarm','th.reminder','th.weather']


def print_predict_commands():
    command = "allennlp predict" \
    " --include-package augment " \
    "--cuda-device 0 " \
    "--use-dataset-reader " \
    "--silent " \
    "--output-file output/{domain}.bert.{exp}.{run_id}.json " \
    "saved_models/snips.bert.{run_id}/{domain}/bert/{exp}/model.tar.gz " \
    "data/snips/{domain}/test.bio"
    for domain in SNIPS_DOMAINS:
        for run_id in ['run1','run2','run3']:
            for exp in ['baseline','1x','2x','4x']:
                print(command.format(run_id=run_id,domain=domain,exp=exp))

def convert_all_to_conll():
    template = "output/{domain}.bert.{exp}.{run_id}.{ext}"
    for domain in SNIPS_DOMAINS:
        for run_id in ['run1','run2','run3']:
            for exp in ['baseline','1x','2x','4x']:
                pred_file = template.format(domain=domain,exp=exp,run_id=run_id,ext='json')
                output_file = template.format(domain=domain,exp=exp,run_id=run_id,ext='conll')
                convert_to_conll_format(pred_file, output_file)


def print_conll_commands():
    template = "{dir}/{domain}.bert.{exp}.{run_id}.{ext}"
    for domain in SNIPS_DOMAINS:
        for run_id in ['run1','run2','run3']:
            for exp in ['baseline','1x','2x','4x']:
                preds_file = template.format(domain=domain,exp=exp,run_id=run_id,ext='conll',dir='output')
                result_file = template.format(domain=domain,exp=exp,run_id=run_id,ext='res',dir='result')
                print("scripts/conlleval < {preds} > {result}".format(preds=preds_file,result=result_file))

if __name__ == '__main__':
    #convert_all_to_conll()
    #print_predict_commands()
    #pred_file = "output.json"
    output_file = "output.conll"
    #convert_to_conll_format(pred_file, output_file)
    #print_conll_commands()




