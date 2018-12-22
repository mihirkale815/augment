TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/train.th.syn_en_th.syn_th_en.syn_th_th_4.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/test-th.conllu \
allennlp train -s saved_models/th.syn_en_th.syn_th_en.syn_th_th_4 training_configs/th.syn_en_th.syn_th_en.syn_th_th_4.jsonnet --include-package augment.dataset_readers
