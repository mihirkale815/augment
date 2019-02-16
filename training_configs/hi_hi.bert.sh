TRAIN_DATA_PATH=data/multilingual_atis/hi/train.hi_en.bio \
DEV_DATA_PATH=data/multilingual_atis/en/dev.bio \
TEST_DATA_PATH=data/multilingual_atis/hi/test.bio \
allennlp train -s saved_models/hi_hi.bert training_configs/atis.bertml.jsonnet --include-package augment.dataset_readers

