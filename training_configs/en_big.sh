TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/train-en.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/eval-en.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/test-en.conllu \
allennlp train -s saved_models/en_big training_configs/en_big.jsonnet --include-package augment.dataset_readers
