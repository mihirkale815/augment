TRAIN_DATA_PATH=data/multilingual_atis/hi/train.hi_en.ours.bio \
DEV_DATA_PATH=data/multilingual_atis/en/dev.bio \
TEST_DATA_PATH=data/multilingual_atis/hi/test.bio \
allennlp train -s saved_models/hi_en.ours.fasttext.ft training_configs/atis.fasttext.jsonnet --include-package augment.dataset_readers

