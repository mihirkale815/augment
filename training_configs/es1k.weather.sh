TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/train-es1k.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/test-es.conllu \
allennlp train -s saved_models/es1k.weather training_configs/es_master.weather.jsonnet --include-package augment.dataset_readers
