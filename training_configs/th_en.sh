TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/train.th.en.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dilsalog_slotfilling/th/test-th.conllu \
allennlp train -s saved_models/th_en training_configs/th_en.jsonnet --include-package augment.dataset_readers
