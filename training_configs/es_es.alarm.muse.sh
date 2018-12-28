TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/train.es.syn_es.1.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/test-es.conllu \
allennlp train -s saved_models/es_es.alarm.muse training_configs/es_master.muse.alarm.jsonnet --include-package augment.dataset_readers
