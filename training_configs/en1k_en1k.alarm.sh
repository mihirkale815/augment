TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/train.en1k.syn_en1k.1.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/eval-en.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/test-en.conllu \
allennlp train -s saved_models/en1k_en1k.alarm training_configs/en_master.alarm.jsonnet --include-package augment.dataset_readers
