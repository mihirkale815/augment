TRAIN_DATA_PATH=data/multilingual_atis/hi/train.hi_hi.4.bio \
DEV_DATA_PATH=data/multilingual_atis/hi/test.bio \
TEST_DATA_PATH=data/multilingual_atis/hi/test.bio \
allennlp train -s saved_models/hi_hi.zemb training_configs/atis.zemb.jsonnet --include-package augment.dataset_readers

