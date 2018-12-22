TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/train.es1k.syn_en_es.syn_es_en.syn_es_es_4.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/test-es.conllu \
allennlp train -s saved_models/es1k.syn_en_es.syn_es_en.syn_es_es_4 training_configs/es1k.syn_en_es.syn_es_en.syn_es_es_4.jsonnet --include-package augment.dataset_readers
