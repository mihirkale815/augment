TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th100/train.th.syn_th.4.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/test-th.conllu \
allennlp train -s saved_models/th100_th.4 training_configs/th100_th.4.jsonnet --include-package augment.dataset_readers
