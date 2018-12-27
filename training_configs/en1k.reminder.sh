TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/train-en1k.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/eval-en.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/test-en.conllu \
allennlp train -s saved_models/en1k.reminder training_configs/en_master.reminder.jsonnet --include-package augment.dataset_readers
