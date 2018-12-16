TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/train.es.syn_all.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/test-es.conllu \
allennlp train -s saved_models/es_all training_configs/es_all.jsonnet --include-package augment.dataset_readers
