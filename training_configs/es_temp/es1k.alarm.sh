TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/train-es.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/test-es.conllu \
allennlp train -s saved_models/es1k.alarm training_configs/es_master.alarm.jsonnet --include-package augment.dataset_readers
