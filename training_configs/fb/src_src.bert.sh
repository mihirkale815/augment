TRAIN_DATA_PATH=data/fb/$1/$2/train.$1_$1.4.bio \
DEV_DATA_PATH=data/fb/$1/$2/dev.bio \
TEST_DATA_PATH=data/fb/$1/$2/test.bio \
allennlp train -s saved_models/fb/$1_$1.$2.bert training_configs/fb.$1.bertml.jsonnet --include-package augment.dataset_readers

