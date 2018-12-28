TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th_clean/train.th.en.syn_en_th.syn_th_en.1.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th_clean/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th_clean/test-th.conllu \
allennlp train -s saved_models/thclean.en.syn_en_th.syn_th_en.reminder training_configs/th_master.reminder.jsonnet --include-package augment.dataset_readers
