TRAIN_DATA_PATH=data/multilingual_atis/$1/train.$1_en.bio \
DEV_DATA_PATH=data/multilingual_atis/$1/dev.bio \
TEST_DATA_PATH=data/multilingual_atis/$1/test.bio \
allennlp train -s saved_models/$1_en.muse training_configs/atis.$1.muse.jsonnet --include-package augment.dataset_readers

