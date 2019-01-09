import sys
sys.path.append("../")
from augment.data.instance import Instance,BIODataUtils,FBDataUtils
import os
from collections import defaultdict
import random




def write_to_file(instance_iterator,out_path):
    fout = open(out_path, "w")
    for instance in instance_iterator:
        fout.write("\n".join(instance.lines) + "\n\n")
    fout.close()







def split_data(in_data_dir,out_data_dir,ds_name):

    train_path = os.path.join(in_data_dir, ds_name, "train.bio")
    dev_path = os.path.join(in_data_dir, ds_name, "dev.bio")
    test_path = os.path.join(in_data_dir, ds_name, "test.bio")

    data_util = BIODataUtils()
    train_igen = data_util.instance_gen(train_path)
    dev_igen = data_util.instance_gen(dev_path)
    test_igen = data_util.instance_gen(test_path)

    train_instances = [instance for instance in train_igen] + [instance for instance in dev_igen]
    random.shuffle(train_instances)

    test_instances = [instance for instance in test_igen]

    num_test = 700
    num_dev = 400
    cutoff_idx = num_dev + num_test - len(test_instances)

    dev_instances = train_instances[:num_dev]
    test_instances = test_instances + train_instances[num_dev:cutoff_idx]
    train_instances = train_instances[cutoff_idx:]

    train_path = os.path.join(out_data_dir, ds_name, "train.bio")
    dev_path = os.path.join(out_data_dir, ds_name, "dev.bio")
    test_path = os.path.join(out_data_dir, ds_name, "test.bio")
    write_to_file(train_instances, train_path)
    write_to_file(test_instances, test_path)
    write_to_file(dev_instances, dev_path)






if __name__ == '__main__':

    split_data(out_data_dir="data/snips",in_data_dir = "data/snips_original/",ds_name = "play_music")
    split_data(out_data_dir="data/snips",in_data_dir="data/snips_original/", ds_name="get_weather")
    split_data(out_data_dir="data/snips",in_data_dir="data/snips_original/", ds_name="rate_book")
    split_data(out_data_dir="data/snips",in_data_dir="data/snips_original/", ds_name="search_creative_work")
    split_data(out_data_dir="data/snips",in_data_dir="data/snips_original/", ds_name="search_screening_event")
    split_data(out_data_dir="data/snips",in_data_dir="data/snips_original/", ds_name="add_to_playlist")
    split_data(out_data_dir="data/snips",in_data_dir="data/snips_original/", ds_name="book_restaurant")

