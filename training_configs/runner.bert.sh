TRAIN_DATA_PATH=data/$1/$2.bio \
DEV_DATA_PATH=data/$1/dev.bio \
TEST_DATA_PATH=data/$1/test.bio \
allennlp train -s saved_models/$1/$3 training_configs/generic.bert.jsonnet --include-package augment.dataset_readers
