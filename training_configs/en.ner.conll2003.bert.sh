alias allennlp='python -m allennlp.run'
TRAIN_DATA_PATH=data/ner/conll2003/eng.train \
DEV_DATA_PATH=data/ner/conll2003/eng.testa \
TEST_DATA_PATH=data/ner/conll2003/eng.testb \
allennlp train -s saved_models/en.ner.conll2003.bert training_configs/en.ner.conll2003.bert.jsonnet --include-package augment.dataset_readers
