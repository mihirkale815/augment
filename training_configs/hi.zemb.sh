TRAIN_DATA_PATH=data/multilingual_atis/hi/train.bio \
DEV_DATA_PATH=data/multilingual_atis/hi/test.bio \
TEST_DATA_PATH=data/multilingual_atis/hi/test.bio \
allennlp train -s saved_models/hi.zemb.ft training_configs/atis.zemb.jsonnet --include-package augment.dataset_readers

