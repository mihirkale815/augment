TRAIN_DATA_PATH=data/multilingual_atis/$1/train.$1_$1.4.bio \
DEV_DATA_PATH=data/multilingual_atis/$1/dev.bio \
TEST_DATA_PATH=data/multilingual_atis/$1/test.bio \
allennlp train -s saved_models/$1_$1.fasttext training_configs/atis.$1.fasttext.jsonnet --include-package augment.dataset_readers

