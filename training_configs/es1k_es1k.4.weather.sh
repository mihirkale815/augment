TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/train.es1k.syn_es1k.4.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/test-es.conllu \
allennlp train -s saved_models/es1k_es1k.4.weather training_configs/es_master.weather.jsonnet --include-package augment.dataset_readers
