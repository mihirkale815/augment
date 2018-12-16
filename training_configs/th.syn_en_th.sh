TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/train.th.syn_en_th.1.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/test-th.conllu \
allennlp train -s saved_models/th.syn_en_th training_configs/th.syn_en_th.jsonnet --include-package augment.dataset_readers
