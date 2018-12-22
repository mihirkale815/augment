TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/train.en.delex.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/eval-en.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/test-en.conllu \
allennlp train -s saved_models/en.delex training_configs/en.delex.jsonnet --include-package augment.dataset_readers
