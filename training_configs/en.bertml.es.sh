TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/train-en.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es/test-es.conllu \
allennlp train -s saved_models/en.bertml.es training_configs/en.bertml.es.jsonnet --include-package augment.dataset_readers
