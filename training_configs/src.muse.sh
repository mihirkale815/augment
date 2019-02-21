TRAIN_DATA_PATH=data/multilingual_atis/$1/train.bio \
DEV_DATA_PATH=data/multilingual_atis/$1/dev.bio \
TEST_DATA_PATH=data/multilingual_atis/$1/test.bio \
allennlp train -s saved_models/$1.muse training_configs/atis.$1.muse.jsonnet --include-package augment.dataset_readers

