TRAIN_DATA_PATH=data/multilingual_atis/$1/train.$1_en.ours.bio \
DEV_DATA_PATH=data/multilingual_atis/$1/dev.bio \
TEST_DATA_PATH=data/multilingual_atis/$1/test.bio \
allennlp train -s saved_models/$1_en.ours.bert training_configs/atis.$1.bertml.jsonnet --include-package augment.dataset_readers


