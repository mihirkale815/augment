TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/train.th.syn_th.1.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/test-th.conllu \
allennlp train -s saved_models/th_th training_configs/th_th.jsonnet --include-package augment.dataset_readers
